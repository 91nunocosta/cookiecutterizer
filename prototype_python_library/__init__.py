"""A library for creating templates or projects from prototype projects."""
from collections import deque
from pathlib import Path
from typing import Dict, Iterator, Tuple

__version__ = "0.1.0"


def create_project(
    seed_project: Path, substitutions: Dict[str, str], destination: Path
):
    """Create a project from a seed prototype project.

    Args:
        seed_project (Path): project to use as prototype.
        substitutions (Dict[str, str]): substitutions to apply to the seed project.
        destination (Path): directory where to create the new project.
    """
    for seed_file, target_file in target_files(
        seed_project, substitutions, destination
    ):
        if seed_file.is_dir():
            target_file.mkdir()
        else:
            create_file(seed_file, substitutions, target_file)


def target(seed: str, substitutions: Dict[str, str]) -> str:
    """Compute target string applying substitutions.

    Args:
        seed (str): seed string.
        substitutions (Dict[str, str]): substitutions to apply.

    Returns:
        target string.
    """
    target = seed

    for old, new in substitutions.items():
        target = target.replace(old, new)

    return target


def target_path(
    root: Path, relative_seed_path: Path, substitutions: Dict[str, str]
) -> Path:
    """Compute target path, applying substitutions.

    Args:
        root (Path): path where the target project is located.
        relative_seed_path (Path): seed path relative to its parent path.
        substitutions (Dict[str, str]): substitutions to apply to the seed project.

    Returns:
        The target path.
    """
    target_parts = [
        target(component, substitutions) for component in relative_seed_path.parts
    ]
    return root.joinpath(*target_parts)


def target_files(
    seed_project: Path, substitutions: Dict[str, str], destination: Path
) -> Iterator[Tuple[Path, Path]]:
    """Obtain the target files for every file in the seed project.

    Args:
        seed_project (Path): project to use as prototype.
        substitutions (Dict[str, str]): substitutions to apply to the seed project.
        destination (Path): directory where to create the new project.

    Yields:
        Pairs of seed file path and target file path.
    """
    frontier = deque([seed_project])

    while frontier:
        path = frontier.popleft()
        relative_seed = seed_project.name / path.relative_to(seed_project)
        target = target_path(destination, relative_seed, substitutions)

        yield (path, target)

        if path.is_dir():
            for children in path.iterdir():
                frontier.append(children)


def create_file(seed_file: Path, substitutions: Dict[str, str], target_file: Path):
    """Create a file from a seed file, applying substitutions.

    Args:
        seed_file: file to use as prototype.
        substitutions: substitutions to apply to the seed project.
        target_file: target file to create.
    """
    with seed_file.open("r") as seed_file_stream:
        with target_file.open("w") as target_file_stream:
            target = seed_file_stream.read()

            for old, new in substitutions.items():
                target = target.replace(old, new)

            target_file_stream.write(target)
