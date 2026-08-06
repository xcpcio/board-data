#!/usr/bin/env python3
"""Validate board data JSON files against xcpcio pydantic models."""

from __future__ import annotations

import json
import os
import re
import sys
from bisect import bisect_right
from dataclasses import asdict, dataclass
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


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    message: str
    line: int | None = None
    location: str | None = None


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


def escape_github_annotation(value: str) -> str:
    return value.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def emit_github_annotation(issue: ValidationIssue) -> None:
    params = [f"file={escape_github_annotation(issue.path)}"]
    if issue.line is not None:
        params.append(f"line={issue.line}")
    title = issue.location or "validation"
    params.append(f"title={escape_github_annotation(title)}")
    message = escape_github_annotation(issue.message)
    click.echo(f"::error {','.join(params)}::{message}", err=True)


def collect_file_issues(path: Path, model: Model, max_errors_per_file: int | None) -> list[ValidationIssue]:
    rel_path = path.as_posix()
    try:
        model.model_validate(json_input(str(path)))
    except json.JSONDecodeError as e:
        return [
            ValidationIssue(
                path=rel_path,
                line=e.lineno,
                location="<json>",
                message=f"invalid JSON: {e.msg}",
            )
        ]
    except ValidationError as e:
        validation_errors = e.errors()
        shown_errors = validation_errors[:max_errors_per_file]
        path_lines = JSONPathLineMapper(path.read_text()).parse() if shown_errors else {}
        issues = [
            ValidationIssue(
                path=rel_path,
                line=get_error_line(error["loc"], path_lines),
                location=format_location(error["loc"]),
                message=error["msg"],
            )
            for error in shown_errors
        ]
        hidden_errors = len(validation_errors) - len(shown_errors)
        if hidden_errors > 0:
            issues.append(
                ValidationIssue(
                    path=rel_path,
                    location="<summary>",
                    message=f"{hidden_errors} more error(s) hidden; use --all-errors to show all",
                )
            )
        return issues

    return []


def report_issues(issues: list[ValidationIssue], *, github_annotations: bool) -> None:
    grouped: dict[str, list[ValidationIssue]] = {}
    for issue in issues:
        grouped.setdefault(issue.path, []).append(issue)

    for path, path_issues in grouped.items():
        real_issues = [issue for issue in path_issues if issue.location != "<summary>"]
        click.secho(f"{path}: validation failed ({len(real_issues)} error(s))", fg="red", err=True)
        for issue in path_issues:
            if issue.location == "<summary>":
                click.echo(f"  ... {issue.message}", err=True)
                continue
            line_prefix = f"line {issue.line}: " if issue.line is not None else ""
            location = issue.location or "<root>"
            click.echo(f"  - {line_prefix}{location}: {issue.message}", err=True)
            if github_annotations:
                emit_github_annotation(issue)


@click.command()
@click.argument(
    "data_dirs",
    nargs=-1,
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
)
@click.option(
    "--max-errors-per-file",
    default=10,
    show_default=True,
    type=click.IntRange(min=0),
    help="Maximum validation errors to display for each invalid file.",
)
@click.option("--all-errors", is_flag=True, help="Display all validation errors for each invalid file.")
@click.option(
    "--report-json",
    type=click.Path(dir_okay=False, writable=True, path_type=Path),
    help="Write machine-readable validation issues to this JSON file.",
)
@click.option(
    "--github-annotations/--no-github-annotations",
    default=None,
    help="Emit GitHub Actions error annotations. Defaults to on when GITHUB_ACTIONS=true.",
)
def validate_data(
    data_dirs: tuple[Path, ...],
    max_errors_per_file: int,
    all_errors: bool,
    report_json: Path | None,
    github_annotations: bool | None,
):
    """Validate config.json, run.json, and team.json files under DATA_DIRS.

    If no DATA_DIRS are given, validates the default ./data directory.
    """
    dirs = data_dirs or (Path("data"),)
    checked = 0
    invalid_files = 0
    issues: list[ValidationIssue] = []
    output_limit = None if all_errors else max_errors_per_file
    use_annotations = (
        bool(os.environ.get("GITHUB_ACTIONS")) if github_annotations is None else github_annotations
    )

    for data_dir in dirs:
        for path, model in iter_target_files(data_dir):
            checked += 1
            file_issues = collect_file_issues(path, model, output_limit)
            if file_issues:
                invalid_files += 1
                issues.extend(file_issues)

    if report_json is not None:
        report_json.parent.mkdir(parents=True, exist_ok=True)
        report_json.write_text(json.dumps([asdict(issue) for issue in issues], indent=2) + "\n")

    if checked == 0:
        click.secho("No target files found.", fg="yellow")
        return

    if issues:
        report_issues(issues, github_annotations=use_annotations)
        click.secho(
            f"\nChecked {checked} file(s), found {invalid_files} invalid file(s).",
            fg="red",
            err=True,
        )
        sys.exit(1)

    click.secho(f"Checked {checked} file(s), all valid.", fg="green")


if __name__ == "__main__":
    validate_data()
