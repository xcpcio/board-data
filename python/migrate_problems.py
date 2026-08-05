#!/usr/bin/env python3
"""Migrate legacy problem_id/balloon_color config fields to problems."""

import json
import sys
from pathlib import Path
from typing import Any

import click
from utils import json_output_for_human_readable


JsonObject = dict[str, Any]


def read_json(path: Path) -> Any:
    with path.open("r") as f:
        return json.load(f)


def write_json(path: Path, data: Any):
    with path.open("w") as f:
        f.write(json_output_for_human_readable(data))


def build_problems(problem_ids: list[Any], balloon_colors: list[Any] | None) -> list[JsonObject]:
    if balloon_colors is not None and len(balloon_colors) != len(problem_ids):
        raise ValueError(
            f"problem_id has {len(problem_ids)} item(s), but balloon_color has {len(balloon_colors)} item(s)"
        )

    problems: list[JsonObject] = []
    for index, label in enumerate(problem_ids):
        problem: JsonObject = {
            "id": str(index),
            "label": str(label),
        }
        if balloon_colors is not None:
            problem["balloon_color"] = balloon_colors[index]
        problems.append(problem)

    return problems


def migrate_config(config: JsonObject) -> tuple[JsonObject, list[Any]]:
    if "problem_id" not in config:
        raise ValueError("missing problem_id")

    problem_ids = config["problem_id"]
    if not isinstance(problem_ids, list):
        raise ValueError("problem_id must be a list")

    balloon_colors = config.get("balloon_color")
    if balloon_colors is not None and not isinstance(balloon_colors, list):
        raise ValueError("balloon_color must be a list")

    problems = build_problems(problem_ids, balloon_colors)
    migrated: JsonObject = {}
    inserted = False

    for key, value in config.items():
        if key == "problem_id":
            migrated["problems"] = problems
            inserted = True
        elif key == "balloon_color":
            continue
        else:
            migrated[key] = value

    if not inserted:
        migrated["problems"] = problems

    return migrated, problem_ids


def remap_problem_id(value: Any, problem_ids: list[Any], label_to_id: dict[str, str]) -> str | None:
    if isinstance(value, bool):
        return None

    if isinstance(value, int):
        if 0 <= value < len(problem_ids):
            return str(value)
        return None

    if isinstance(value, str):
        if value in label_to_id:
            return label_to_id[value]
        if value.isdecimal():
            index = int(value)
            if 0 <= index < len(problem_ids):
                return str(index)

    return None


def migrate_submissions(submissions: Any, problem_ids: list[Any]) -> int:
    if not isinstance(submissions, list):
        raise ValueError("run.json must be a list")

    label_to_id = {str(label): str(index) for index, label in enumerate(problem_ids)}
    changed = 0
    for index, submission in enumerate(submissions):
        if not isinstance(submission, dict) or "problem_id" not in submission:
            continue

        old_problem_id = submission["problem_id"]
        new_problem_id = remap_problem_id(old_problem_id, problem_ids, label_to_id)
        if new_problem_id is None:
            raise ValueError(f"run.json[{index}].problem_id cannot be mapped: {old_problem_id!r}")

        if old_problem_id != new_problem_id:
            submission["problem_id"] = new_problem_id
            changed += 1

    return changed


def iter_config_paths(data_dir: Path):
    for config_path in sorted(data_dir.rglob("config.json")):
        if config_path.is_file():
            yield config_path


def migrate_board(config_path: Path, write: bool) -> tuple[bool, str]:
    config = read_json(config_path)
    if not isinstance(config, dict):
        raise ValueError("config.json must be an object")

    has_legacy_fields = "problem_id" in config or "balloon_color" in config
    if not has_legacy_fields:
        return False, "skip: no legacy problem fields"

    if "problem_id" not in config and "balloon_color" in config:
        raise ValueError("has balloon_color but missing problem_id")

    migrated_config, problem_ids = migrate_config(config)
    run_path = config_path.with_name("run.json")
    run_changed = 0
    migrated_submissions = None

    if run_path.exists():
        migrated_submissions = read_json(run_path)
        run_changed = migrate_submissions(migrated_submissions, problem_ids)

    if write:
        write_json(config_path, migrated_config)
        if migrated_submissions is not None:
            write_json(run_path, migrated_submissions)

    action = "migrated" if write else "would migrate"
    detail = f"{action}: {len(problem_ids)} problem(s)"
    if run_path.exists() and write:
        detail += f", {run_changed} run problem_id value(s)"
    elif run_path.exists():
        detail += ", run.json checked"

    return True, detail


@click.command()
@click.argument(
    "data_dir",
    default="data",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
)
@click.option("--write", is_flag=True, help="Write migrated config.json and run.json files. Defaults to dry-run.")
def migrate_problems(data_dir: Path, write: bool):
    """Convert legacy board problem fields under DATA_DIR to the problems format."""
    migrated = 0
    skipped = 0
    errors = 0

    for config_path in iter_config_paths(data_dir):
        try:
            changed, message = migrate_board(config_path, write)
        except Exception as e:
            errors += 1
            click.secho(f"{config_path}: error: {e}", fg="red", err=True)
            continue

        if changed:
            migrated += 1
            click.echo(f"{config_path}: {message}")
        else:
            skipped += 1

    mode = "write" if write else "dry-run"
    click.echo(f"\nMode: {mode}. Migrated: {migrated}. Skipped: {skipped}. Errors: {errors}.")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    migrate_problems()
