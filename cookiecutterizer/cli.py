"""Command Line Interface."""
import json
from pathlib import Path

import click

from cookiecutterizer import create_project


@click.command()
@click.option("--substitutions", type=click.File(), required=True)
@click.option("--destination", type=click.Path(), required=True)
@click.argument("project", type=click.Path())
#  pylint: disable=unused-argument
def cookiecutterize(project, substitutions, destination):
    """Run the cookiecutterize.

    Args:
        project (click.Path): source project.
        substitutions (click.File): json file with the substitutions to apply.
        destination: (click.Path): destination directory
    """
    create_project(Path(project), json.load(substitutions), Path(destination))
