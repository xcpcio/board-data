#!/usr/bin/env python3
"""Post board-data validation issues as inline PR review comments."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import click

MARKER = "<!-- board-data-validate -->"
HUNK_HEADER_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")
MAX_INLINE_COMMENTS = 30


def run_gh(args: list[str], *, input_text: str | None = None) -> str:
    result = subprocess.run(
        ["gh", *args],
        input=input_text,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"gh {' '.join(args)} failed")
    return result.stdout


def parse_commentable_lines(patch: str | None) -> set[int]:
    """Return RIGHT-side line numbers that GitHub accepts for review comments."""
    if not patch:
        return set()

    lines: set[int] = set()
    new_line: int | None = None
    for raw in patch.splitlines():
        header = HUNK_HEADER_RE.match(raw)
        if header:
            new_line = int(header.group(1))
            continue
        if new_line is None or raw.startswith("\\"):
            continue
        if raw.startswith("+"):
            lines.add(new_line)
            new_line += 1
        elif raw.startswith("-"):
            continue
        else:
            # context line — also commentable on the RIGHT side
            lines.add(new_line)
            new_line += 1
    return lines


def load_issues(report_path: Path) -> list[dict[str, Any]]:
    data = json.loads(report_path.read_text())
    if not isinstance(data, list):
        raise click.ClickException("report JSON must be a list of issues")
    return [issue for issue in data if issue.get("location") != "<summary>"]


def delete_previous_comments(owner: str, repo: str, pr_number: int) -> None:
    output = run_gh(
        [
            "api",
            "--paginate",
            f"repos/{owner}/{repo}/pulls/{pr_number}/comments",
        ]
    )
    if not output.strip():
        return

    for comment in json.loads(output):
        body = comment.get("body") or ""
        if MARKER not in body:
            continue
        run_gh(["api", "-X", "DELETE", f"repos/{owner}/{repo}/pulls/comments/{comment['id']}"])


def issue_fingerprint(issue: dict[str, Any]) -> tuple[str, str]:
    return (issue.get("location") or "<root>", issue.get("message") or "validation failed")


def group_issues_by_line(issues: list[dict[str, Any]]) -> list[tuple[str, int | None, list[dict[str, Any]]]]:
    """Group issues by (path, line), preserving first-seen order and deduping identical messages."""
    grouped: dict[tuple[str, int | None], list[dict[str, Any]]] = {}
    order: list[tuple[str, int | None]] = []
    seen: set[tuple[str, int | None, str, str]] = set()

    for issue in issues:
        path = issue["path"]
        line = issue.get("line")
        location, message = issue_fingerprint(issue)
        key = (path, line, location, message)
        if key in seen:
            continue
        seen.add(key)

        group_key = (path, line if isinstance(line, int) else None)
        if group_key not in grouped:
            grouped[group_key] = []
            order.append(group_key)
        grouped[group_key].append(issue)

    return [(path, line, grouped[(path, line)]) for path, line in order]


def build_comment_body(issues: list[dict[str, Any]]) -> str:
    lines = [MARKER, f"**validate-data**: {len(issues)} issue(s)"]
    for issue in issues:
        location, message = issue_fingerprint(issue)
        lines.append(f"- `{location}` — {message}")
    return "\n".join(lines)


def format_unmatched_group(path: str, line: int | None, issues: list[dict[str, Any]]) -> str:
    line_text = f":{line}" if line is not None else ""
    details = "; ".join(f"`{loc}` — {msg}" for loc, msg in (issue_fingerprint(i) for i in issues))
    return f"- `{path}{line_text}`: {details}"


@click.command()
@click.argument("report_json", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--owner", default=None, help="Repository owner. Defaults to GITHUB_REPOSITORY.")
@click.option("--repo", default=None, help="Repository name. Defaults to GITHUB_REPOSITORY.")
@click.option("--pr", "pr_number", type=int, default=None, help="PR number. Defaults to event payload.")
@click.option("--commit", "commit_id", default=None, help="Head commit SHA. Defaults to GITHUB_SHA.")
def post_validate_pr_comments(
    report_json: Path,
    owner: str | None,
    repo: str | None,
    pr_number: int | None,
    commit_id: str | None,
) -> None:
    """Create a PR review with inline comments from a validate_data JSON report."""
    repository = os.environ.get("GITHUB_REPOSITORY", "")
    if owner is None or repo is None:
        if "/" not in repository:
            raise click.ClickException("Set --owner/--repo or GITHUB_REPOSITORY")
        default_owner, default_repo = repository.split("/", 1)
        owner = owner or default_owner
        repo = repo or default_repo

    if pr_number is None:
        event_path = os.environ.get("GITHUB_EVENT_PATH")
        if not event_path:
            raise click.ClickException("Set --pr or provide GITHUB_EVENT_PATH")
        event = json.loads(Path(event_path).read_text())
        pr_number = (event.get("pull_request") or {}).get("number")
        if pr_number is None:
            raise click.ClickException("No pull_request.number in GitHub event payload")

    commit_id = commit_id or os.environ.get("GITHUB_SHA")
    if not commit_id:
        raise click.ClickException("Set --commit or GITHUB_SHA")

    issues = load_issues(report_json)
    delete_previous_comments(owner, repo, pr_number)

    if not issues:
        click.echo("No issues to comment on; cleared previous validate comments.")
        return

    files_json = run_gh(["api", "--paginate", f"repos/{owner}/{repo}/pulls/{pr_number}/files"])
    commentable: dict[str, set[int]] = {}
    for file_info in json.loads(files_json):
        commentable[file_info["filename"]] = parse_commentable_lines(file_info.get("patch"))

    review_comments: list[dict[str, Any]] = []
    unmatched_groups: list[tuple[str, int | None, list[dict[str, Any]]]] = []
    issue_count = 0

    for path, line, group in group_issues_by_line(issues):
        issue_count += len(group)
        if (
            isinstance(line, int)
            and line in commentable.get(path, set())
            and len(review_comments) < MAX_INLINE_COMMENTS
        ):
            review_comments.append(
                {
                    "path": path,
                    "line": line,
                    "side": "RIGHT",
                    "body": build_comment_body(group),
                }
            )
        else:
            unmatched_groups.append((path, line, group))

    body_lines = [
        MARKER,
        "## validate-data",
        "",
        f"Found **{issue_count}** validation issue(s) across **{len(review_comments) + len(unmatched_groups)}** location(s).",
    ]
    if unmatched_groups:
        body_lines.extend(["", "Issues outside the PR diff (see workflow annotations):", ""])
        for path, line, group in unmatched_groups[:50]:
            body_lines.append(format_unmatched_group(path, line, group))
        if len(unmatched_groups) > 50:
            body_lines.append(f"- ... and {len(unmatched_groups) - 50} more location(s)")

    payload: dict[str, Any] = {
        "commit_id": commit_id,
        "body": "\n".join(body_lines),
        "event": "COMMENT",
        "comments": review_comments,
    }

    run_gh(
        ["api", "--method", "POST", f"repos/{owner}/{repo}/pulls/{pr_number}/reviews", "--input", "-"],
        input_text=json.dumps(payload),
    )
    click.echo(
        f"Posted review on PR #{pr_number}: {len(review_comments)} inline comment(s), "
        f"{len(unmatched_groups)} summarized outside diff."
    )


if __name__ == "__main__":
    try:
        post_validate_pr_comments()
    except RuntimeError as exc:
        click.secho(str(exc), fg="red", err=True)
        sys.exit(1)
