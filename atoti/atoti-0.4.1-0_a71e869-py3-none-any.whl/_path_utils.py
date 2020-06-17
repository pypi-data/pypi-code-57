"""Utilities for handling file paths."""

import os
from pathlib import Path
from typing import Union

PathLike = Union[str, Path]


def get_atoti_home() -> Path:
    """Get the path from $ATOTI_HOME env variable. If not defined, use $HOME/.atoti."""
    if "ATOTI_HOME" in os.environ:
        return Path(os.environ["ATOTI_HOME"])
    return Path.home() / ".atoti"


def stem_path(path: PathLike) -> str:
    """Return the final path component, without its suffix."""
    # Handle Path objects
    if isinstance(path, Path):
        return path.stem

    # Handle plain strings
    if isinstance(path, str):
        if path.startswith("s3://"):
            return path[path.rfind("/") + 1 :]
        return stem_path(Path(path))

    raise ValueError(
        f"path should be either of type str or pathlib.Path. It is {type(path)}"
    )


def to_absolute_path(path: PathLike) -> str:
    """Transform the input path-like object into an absolute path.

    Args:
        path: A path-like object that points either to a local file
            or an AWS S3 file.

    """
    # Handle Path objects
    if isinstance(path, Path):
        return str(path.resolve())

    # Handle plain strings
    if isinstance(path, str):
        if path.startswith("s3://"):
            return path
        return str(Path(path).resolve())

    raise ValueError(
        f"path should be either of type str or pathlib.Path. It is {type(path)}"
    )


def to_posix_path(path: PathLike) -> str:
    """Transform the input path-like object into a posix path.

    Args:
        path: A path-like object that points either to a local file or an AWS file
    """
    # Handle Path objects
    if isinstance(path, Path):
        return str(path.as_posix())

    # Handle plain paths
    if isinstance(path, str):
        if path.startswith("s3://"):
            return path

        return str(Path(path).resolve().as_posix())

    raise ValueError(
        f"path should be either of type str or pathlib.Path. It is {type(path)}"
    )
