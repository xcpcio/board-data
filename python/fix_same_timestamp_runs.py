#!/usr/bin/env python3
"""Fix contests whose runs collapse every team-problem onto one timestamp.

Some historical boards only recorded the last / AC time, then copied that timestamp
onto every submission of the same team and problem. The new rank calculator treats
same-timestamp submissions by result priority, and ACCEPTED wins, so those wrong
submissions no longer produce penalty.

For affected contests, set non-accepted, non-pending timestamps to 0 so penalty
still counts and the AC time is unchanged.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import click
from utils import json_input, json_output_for_human_readable

ACCEPTED = "ACCEPTED"
PENDING = "PENDING"


def is_penalty_status(status: object) -> bool:
    return status not in (ACCEPTED, PENDING, None)


def group_runs_by_team_problem(runs: list) -> dict[tuple[str, str], list]:
    groups: dict[tuple[str, str], list] = defaultdict(list)
    for run in runs:
        if not isinstance(run, dict):
            continue
        groups[(str(run.get("team_id")), str(run.get("problem_id")))].append(run)
    return groups


def is_collapsed_timestamp_contest(runs: list) -> bool:
    """True if every mixed AC + penalty group shares a single timestamp."""
    if not isinstance(runs, list) or not runs:
        return False

    mixed_same = 0
    mixed_diff = 0
    for items in group_runs_by_team_problem(runs).values():
        if len(items) < 2:
            continue
        statuses = {item.get("status") for item in items}
        if ACCEPTED not in statuses or not any(is_penalty_status(status) for status in statuses):
            continue
        timestamps = {item.get("timestamp") for item in items}
        if len(timestamps) == 1:
            mixed_same += 1
        else:
            mixed_diff += 1

    return mixed_same > 0 and mixed_diff == 0


def fix_collapsed_timestamps(runs: list) -> int:
    """Set penalty submission timestamps to 0. Returns the number of changed runs."""
    changed = 0
    for run in runs:
        if not isinstance(run, dict):
            continue
        if is_penalty_status(run.get("status")) and run.get("timestamp") != 0:
            run["timestamp"] = 0
            changed += 1
    return changed


@click.command()
@click.argument("dir", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option(
    "--check",
    is_flag=True,
    help="List affected contests; do not write.",
)
def main(dir: str, check: bool):
    dir_path = Path(dir)
    run_files = sorted(dir_path.rglob("run.json"))

    if not run_files:
        click.echo(f"No run.json files found in '{dir}'")
        return

    affected = 0
    changed_runs = 0
    errors: list[tuple[Path, Exception]] = []

    for run_file in run_files:
        try:
            runs = json_input(str(run_file))
        except Exception as e:
            errors.append((run_file, e))
            click.secho(f"{run_file} ✗ Error: {e}", fg="red")
            continue

        if not is_collapsed_timestamp_contest(runs):
            continue

        affected += 1
        if check:
            click.echo(str(run_file))
            continue

        n = fix_collapsed_timestamps(runs)
        changed_runs += n
        with open(run_file, "w") as f:
            f.write(json_output_for_human_readable(runs))
        click.echo(f"{run_file}  changed {n} rejected timestamp(s)")

    if errors:
        click.secho(f"\n{len(errors)} file(s) failed to parse.", fg="red", err=True)

    if check:
        click.secho(f"\nFound {affected} collapsed-timestamp contest(s).", fg="green")
        return

    click.secho(
        f"\nFixed {affected} contest(s), {changed_runs} rejected timestamp(s).",
        fg="green",
    )


if __name__ == "__main__":
    main()
