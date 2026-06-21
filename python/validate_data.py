#!/usr/bin/env python3
"""Validate board data JSON files against xcpcio pydantic models."""

import json
import sys
from pathlib import Path
from typing import Iterable

import click
from pydantic import BaseModel, ValidationError
from utils import json_input
from xcpcio.types import Contest, Organizations, SeatMap, Submissions, Teams

Model = type[BaseModel]

TARGETS: dict[str, Model] = {
    "config.json": Contest,
    "run.json": Submissions,
    "team.json": Teams,
    "seat_map.json": SeatMap,
    "organizations.json": Organizations,
}


def iter_target_files(data_dir: Path) -> Iterable[tuple[Path, Model]]:
    for file_name, model in TARGETS.items():
        for path in sorted(data_dir.rglob(file_name)):
            yield path, model


def format_location(location: tuple[int | str, ...]) -> str:
    if not location:
        return "<root>"

    parts: list[str] = []
    for item in location:
        if isinstance(item, int):
            parts.append(f"[{item}]")
        elif not parts:
            parts.append(str(item))
        else:
            parts.append(f".{item}")

    return "".join(parts)


def validate_file(path: Path, model: Model, max_errors_per_file: int | None) -> int:
    try:
        model.model_validate(json_input(str(path)))
    except json.JSONDecodeError as e:
        click.secho(f"{path}: invalid JSON: {e}", fg="red", err=True)
        return 1
    except ValidationError as e:
        validation_errors = e.errors()
        shown_errors = validation_errors[:max_errors_per_file]

        click.secho(f"{path}: validation failed ({len(validation_errors)} error(s))", fg="red", err=True)
        for error in shown_errors:
            location = format_location(error["loc"])
            message = error["msg"]
            click.echo(f"  - {location}: {message}", err=True)

        hidden_errors = len(validation_errors) - len(shown_errors)
        if hidden_errors > 0:
            click.echo(f"  ... {hidden_errors} more error(s) hidden; use --all-errors to show all", err=True)
        return 1

    return 0


@click.command()
@click.argument(
    "data_dir", default="data", type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path)
)
@click.option(
    "--max-errors-per-file",
    default=10,
    show_default=True,
    type=click.IntRange(min=0),
    help="Maximum validation errors to display for each invalid file.",
)
@click.option("--all-errors", is_flag=True, help="Display all validation errors for each invalid file.")
def validate_data(data_dir: Path, max_errors_per_file: int, all_errors: bool):
    """Validate config.json, run.json, and team.json files under DATA_DIR."""
    checked = 0
    errors = 0
    output_limit = None if all_errors else max_errors_per_file

    for path, model in iter_target_files(data_dir):
        checked += 1
        errors += validate_file(path, model, output_limit)

    if errors:
        click.secho(f"\nChecked {checked} file(s), found {errors} invalid file(s).", fg="red", err=True)
        sys.exit(1)

    click.secho(f"Checked {checked} file(s), all valid.", fg="green")


if __name__ == "__main__":
    validate_data()
