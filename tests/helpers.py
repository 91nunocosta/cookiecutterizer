import shutil
import textwrap
from pathlib import Path
from typing import Optional


def create_text_file(directory: Path, file_name: str, content: str) -> Path:
    if not directory.exists():
        directory.mkdir(parents=True)

    path = directory / file_name

    with path.open("w") as text_file:
        text_file.write(textwrap.dedent(content))

    return path


def create_binary_file(directory: Path, file_name: str) -> Path:
    if not directory.exists():
        directory.mkdir(parents=True)

    path = directory / file_name

    shutil.copy(Path(__file__).parent / "data" / "bin", path)

    return path


#  pylint: disable=unsubscriptable-object
def load_text_file(directory: Path, file_name: str) -> Optional[str]:
    path = directory / file_name

    if not path.exists():
        return None

    with path.open("r") as text_file:
        return text_file.read()
