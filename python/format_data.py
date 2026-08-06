import sys
from pathlib import Path

import click
from utils import json_input, json_output_for_human_readable


@click.command()
@click.argument("dir", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option(
    "--check",
    is_flag=True,
    help="Check that JSON files match json_output_for_human_readable; do not write.",
)
def format_json_files(dir: str, check: bool):
    """Format all JSON files in the given directory using json_output_for_human_readable."""
    dir_path = Path(dir)
    json_files = sorted(dir_path.rglob("*.json"))

    if not json_files:
        click.echo(f"No JSON files found in '{dir}'")
        return

    click.echo(f"Found {len(json_files)} JSON file(s) in '{dir}'")

    mismatched: list[Path] = []
    errors: list[tuple[Path, Exception]] = []

    for json_file in json_files:
        try:
            data = json_input(str(json_file))
            formatted_content = json_output_for_human_readable(data)

            if check:
                actual = json_file.read_text()
                if actual != formatted_content:
                    mismatched.append(json_file)
                    click.secho(f"Would reformat {json_file}", fg="red")
                continue

            click.echo(f"Formatting {json_file}...", nl=False)
            with open(json_file, "w") as f:
                f.write(formatted_content)
            click.secho(" ✓", fg="green")
        except Exception as e:
            errors.append((json_file, e))
            click.secho(f"{'Checking' if check else 'Formatting'} {json_file} ✗ Error: {e}", fg="red")

    if errors:
        click.secho(f"\n{len(errors)} file(s) failed to parse.", fg="red", err=True)
        sys.exit(1)

    if check:
        if mismatched:
            click.secho(
                f"\n{len(mismatched)} file(s) would be reformatted. Run: uv run ./python/format_data.py {dir}",
                fg="red",
                err=True,
            )
            sys.exit(1)
        click.secho(f"Checked {len(json_files)} file(s), all formatted.", fg="green")
        return


if __name__ == "__main__":
    format_json_files()
