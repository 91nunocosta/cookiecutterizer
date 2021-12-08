"""Command Line Interface."""
import json
from pathlib import Path

import click

from prototype_python_library import create_project


@click.command()
@click.option("--substitutions", type=click.File(), required=True)
@click.option("--destination", type=click.Path(), required=True)
@click.argument("project", type=click.Path())
#  pylint: disable=unused-argument
def coockiecutterize(project, substitutions, destination):
    """Run the coockiecutterize.

    Args:
        project (click.Path): source project.
        substitutions (click.File): json file with the substitutions to apply.
        destination: (click.Path): destination directory
    """
    create_project(Path(project), json.load(substitutions), Path(destination))
