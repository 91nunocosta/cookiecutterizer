"""Test prototype_python_library module."""
import textwrap
from pathlib import Path

from prototype_python_library import create_file, target_files
from tests.helpers import create_text_file, load_text_file


def create_emtpy_file(path: Path):
    with path.open("w"):
        pass


def test_target_files(tmp_path):
    """Test function."""
    destination = tmp_path / "destination"

    seed_project = tmp_path / "project"

    seed_project.mkdir()
    (seed_project / "dir1").mkdir()
    (seed_project / "dir2").mkdir()
    create_emtpy_file(seed_project / "file")
    (seed_project / "dir2" / "dir1").mkdir()
    (seed_project / "dir2" / "dir2").mkdir()
    create_emtpy_file(seed_project / "dir2" / "file")

    result = list(target_files(seed_project, {}, destination))

    assert len(result) == 7

    assert set(result) == {
        (seed_project, destination / "project"),
        (seed_project / "dir1", destination / "project" / "dir1"),
        (seed_project / "dir2", destination / "project" / "dir2"),
        (seed_project / "file", destination / "project" / "file"),
        (seed_project / "dir2" / "dir1", destination / "project" / "dir2" / "dir1"),
        (seed_project / "dir2" / "dir2", destination / "project" / "dir2" / "dir2"),
        (seed_project / "dir2" / "file", destination / "project" / "dir2" / "file"),
    }


def test_target_files_with_replacement(tmp_path):
    """Test function."""
    destination = tmp_path / "destination"

    seed_project = tmp_path / "project"

    seed_project.mkdir()
    (seed_project / "dir1").mkdir()
    (seed_project / "dir2").mkdir()
    create_emtpy_file(seed_project / "file")
    (seed_project / "dir2" / "dir1").mkdir()
    (seed_project / "dir2" / "dir2").mkdir()
    create_emtpy_file(seed_project / "dir2" / "file")

    result = list(
        target_files(seed_project, {"dir": "directory", "file": "f"}, destination)
    )

    assert len(result) == 7

    assert set(result) == {
        (seed_project, destination / "project"),
        (seed_project / "dir1", destination / "project" / "directory1"),
        (seed_project / "dir2", destination / "project" / "directory2"),
        (seed_project / "file", destination / "project" / "f"),
        (
            seed_project / "dir2" / "dir1",
            destination / "project" / "directory2" / "directory1",
        ),
        (
            seed_project / "dir2" / "dir2",
            destination / "project" / "directory2" / "directory2",
        ),
        (seed_project / "dir2" / "file", destination / "project" / "directory2" / "f"),
    }


def test_create_file_with_empty_substiutions(tmp_path):
    """Test creating file from seed, applying substitutions."""
    seed_file = create_text_file(
        tmp_path,
        "seed.txt",
        """
        line1
        line2
        ...
        linen
        """,
    )
    create_file(seed_file, {}, tmp_path / "target.txt")

    assert (tmp_path / "target.txt").exists()

    assert load_text_file(tmp_path, "target.txt") == textwrap.dedent(
        """
        line1
        line2
        ...
        linen
        """
    )


def test_create_file_with_substiutions(tmp_path):
    """Test creating file from seed, applying substitutions."""
    seed_file = create_text_file(
        tmp_path,
        "seed.txt",
        """
        line1
        line2
        ...
        linen
        """,
    )
    create_file(seed_file, {"line": "enil"}, tmp_path / "target.txt")

    assert (tmp_path / "target.txt").exists()

    assert load_text_file(tmp_path, "target.txt") == textwrap.dedent(
        """
        enil1
        enil2
        ...
        eniln
        """
    )
