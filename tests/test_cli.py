"""Test Command Line Interface."""
import json
import textwrap
from pathlib import Path

from click.testing import CliRunner

from cookiecutterizer.cli import cookiecutterize
from tests.helpers import create_text_file, load_text_file


def test_cookiecutterize(tmp_path):
    """Test cookiecutterize command."""
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path) as test_directory_path:
        test_directory = Path(test_directory_path)

        project = test_directory / "project"
        destination = test_directory / "destination"

        project.mkdir()
        destination.mkdir()

        substitutions = create_text_file(
            test_directory,
            "substitutions.json",
            json.dumps(
                {
                    "cookiecutterizer": "cookiecutterizer",
                }
            ),
        )

        create_text_file(
            project,
            "pyproject.toml",
            """
            [tool.poetry]
            name = "cookiecutterizer"
            """,
        )

        create_text_file(
            project / "cookiecutterizer",
            "__init__.py",
            """
            __version__ = 0.1.0
            """,
        )

        create_text_file(
            project / "tests",
            "test_cookiecutterizer.py",
            """
            from cookiecutterizer import __version__

            def test_version():
                assert __version__ == "0.1.0"
            """,
        )

        result = runner.invoke(
            cookiecutterize,
            [
                "--substitutions",
                str(substitutions),
                "--destination",
                str(destination),
                str(project),
            ],
        )

    assert result.exit_code == 0
    assert result.output == ""

    target_project = destination / "project"

    assert target_project.exists()

    assert load_text_file(target_project, "pyproject.toml") == textwrap.dedent(
        """
            [tool.poetry]
            name = "cookiecutterizer"
            """
    )

    assert load_text_file(
        target_project / "cookiecutterizer", "__init__.py"
    ) == textwrap.dedent(
        """
            __version__ = 0.1.0
            """
    )

    assert load_text_file(
        target_project / "tests", "test_cookiecutterizer.py"
    ) == textwrap.dedent(
        """
            from cookiecutterizer import __version__

            def test_version():
                assert __version__ == "0.1.0"
            """
    )
