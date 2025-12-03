from pathlib import Path

import click
from utils import json_input, json_output_for_human_readable


@click.command()
@click.argument("dir", type=click.Path(exists=True, file_okay=False, dir_okay=True))
def format_json_files(dir: str):
    """Format all JSON files in the given directory using json_output_for_human_readable."""
    dir_path = Path(dir)
    json_files = list(dir_path.rglob("*.json"))

    if not json_files:
        click.echo(f"No JSON files found in '{dir}'")
        return

    click.echo(f"Found {len(json_files)} JSON file(s) in '{dir}'")

    for json_file in json_files:
        try:
            click.echo(f"Formatting {json_file}...", nl=False)
            data = json_input(str(json_file))
            formatted_content = json_output_for_human_readable(data)

            with open(json_file, "w") as f:
                f.write(formatted_content)

            click.secho(" ✓", fg="green")
        except Exception as e:
            click.secho(f" ✗ Error: {e}", fg="red")


if __name__ == "__main__":
    format_json_files()
