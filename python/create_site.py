#!/usr/bin/env python3
"""Create site directory and prepare all JSON files for deployment."""

import shutil
import sys
from pathlib import Path

import click
from utils import json_input, json_output


def create_site_dir():
    """Create site directory and copy data into it."""
    site_dir = Path("site")
    data_dir = Path("data")

    # Create site directory
    if site_dir.exists():
        click.echo(f"Removing existing {site_dir}")
        shutil.rmtree(site_dir)

    site_dir.mkdir(exist_ok=True)
    click.echo(f"Created {site_dir}")

    # Copy data to site/data
    if not data_dir.exists():
        click.secho(f"Error: {data_dir} does not exist", fg="red", err=True)
        sys.exit(1)

    shutil.copytree(data_dir, site_dir / "data")
    click.echo(f"Copied {data_dir} to {site_dir}/data")


def reformat_json_files():
    """Reformat all JSON files in site/data using json_output."""
    base_dir = Path("site/data")

    if not base_dir.exists():
        click.secho(f"Error: {base_dir} does not exist", fg="red", err=True)
        sys.exit(1)

    count = 0
    errors = 0

    for json_file in base_dir.rglob("*.json"):
        try:
            data = json_input(str(json_file))
            with open(json_file, "w") as f:
                f.write(json_output(data))
            count += 1
            if count % 100 == 0:
                click.echo(f"Processed {count} files...")
        except Exception as e:
            click.secho(f"Error processing {json_file}: {e}", fg="yellow", err=True)
            errors += 1

    click.echo(f"\nTotal JSON files reformatted: {count}")
    if errors > 0:
        click.secho(f"Errors encountered: {errors}", fg="yellow", err=True)


if __name__ == "__main__":
    click.echo("Creating site directory...")
    create_site_dir()

    click.echo("\nReformatting JSON files...")
    reformat_json_files()

    click.secho("\nSite directory created successfully!", fg="green")
