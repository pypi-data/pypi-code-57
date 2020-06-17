"""Module to copy the tutorial notebooks from the atoti package."""

from pathlib import Path
from shutil import copytree, ignore_patterns
from typing import Union

_NOTEBOOKS_DIRECTORY = Path(Path(__file__).parent) / "notebooks"
_TUTORIAL_DIRECTORY = _NOTEBOOKS_DIRECTORY / "tutorial"


def copy_tutorial(path: Union[Path, str]):
    """Copy the tutorial files to the given path."""
    copytree(_TUTORIAL_DIRECTORY, path, ignore=ignore_patterns(".ipynb_checkpoints"))
