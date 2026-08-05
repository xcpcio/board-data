#!/usr/bin/env python3
"""Validate board data JSON files against xcpcio pydantic models."""

import json
import re
import sys
from bisect import bisect_right
from pathlib import Path
from typing import Iterable

import click
from pydantic import BaseModel, ValidationError
from utils import json_input
from xcpcio.types import Contest, Organizations, SeatMap, Submissions, Teams

Model = type[BaseModel]
Location = tuple[int | str, ...]

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


def format_location(location: Location) -> str:
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


class JSONPathLineMapper:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line_starts = [0]
        self.path_lines: dict[Location, int] = {}

        for match in re.finditer("\n", text):
            self.line_starts.append(match.end())

    def line_for(self, pos: int) -> int:
        return bisect_right(self.line_starts, pos)

    def skip_whitespace(self) -> None:
        while self.pos < len(self.text) and self.text[self.pos] in " \t\r\n":
            self.pos += 1

    def parse(self) -> dict[Location, int]:
        self.skip_whitespace()
        self.parse_value(())
        return self.path_lines

    def parse_value(self, location: Location) -> None:
        self.skip_whitespace()
        self.path_lines[location] = self.line_for(self.pos)

        char = self.text[self.pos]
        if char == "{":
            self.parse_object(location)
        elif char == "[":
            self.parse_array(location)
        elif char == '"':
            self.parse_string()
        elif char in "-0123456789":
            self.parse_number()
        else:
            self.parse_literal()

    def parse_object(self, location: Location) -> None:
        self.pos += 1
        self.skip_whitespace()
        if self.text[self.pos] == "}":
            self.pos += 1
            return

        while True:
            self.skip_whitespace()
            key = self.parse_string()
            self.skip_whitespace()
            self.pos += 1
            self.parse_value((*location, key))
            self.skip_whitespace()

            if self.text[self.pos] == "}":
                self.pos += 1
                return

            self.pos += 1

    def parse_array(self, location: Location) -> None:
        self.pos += 1
        self.skip_whitespace()
        if self.text[self.pos] == "]":
            self.pos += 1
            return

        index = 0
        while True:
            self.parse_value((*location, index))
            self.skip_whitespace()

            if self.text[self.pos] == "]":
                self.pos += 1
                return

            self.pos += 1
            index += 1

    def parse_string(self) -> str:
        value, end = json.decoder.scanstring(self.text, self.pos + 1)
        self.pos = end
        return value

    def parse_number(self) -> None:
        match = re.match(r"-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?", self.text[self.pos :])
        if match is None:
            return
        self.pos += len(match.group(0))

    def parse_literal(self) -> None:
        for literal in ("true", "false", "null"):
            if self.text.startswith(literal, self.pos):
                self.pos += len(literal)
                return


def get_error_line(location: Location, path_lines: dict[Location, int]) -> int | None:
    for length in range(len(location), -1, -1):
        if location[:length] in path_lines:
            return path_lines[location[:length]]
    return None


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
        path_lines = JSONPathLineMapper(path.read_text()).parse() if shown_errors else {}
        for error in shown_errors:
            location = format_location(error["loc"])
            line = get_error_line(error["loc"], path_lines)
            message = error["msg"]
            line_prefix = f"line {line}: " if line is not None else ""
            click.echo(f"  - {line_prefix}{location}: {message}", err=True)

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
