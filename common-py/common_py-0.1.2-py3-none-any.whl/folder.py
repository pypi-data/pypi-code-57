import os
from pathlib import Path
from typing import Callable, List

import toolz
from toolz import curry

import common_py
from common_py.either import Either, Left, Right


def files_in_folder(
    folder_name: str,
    include_hidden_file: bool = False,
    filters: List[Callable[[str], bool]] = [],
) -> List[str]:
    """
    Get files in folder.

    Parameters
    ----------
    folder_name : str
        Folder name
    include_hidden_file : bool, optional
        Whether hidden files are included(starts with '.'), by default False
    filters : List[Callable[[str], bool]], optional
        Filters to apply to result, by default []

    Returns
    -------
    List[str]
        File list

    Notes
    -----
    .. versionadded:: 0.1.0
    """
    # file only
    filters2: List[Callable[[str], bool]] = filters.copy()
    filters2.append(lambda f: os.path.isfile(folder_name + "/" + f))
    # hidden file filter
    if include_hidden_file is False:
        filters2.append(lambda file_name: not file_name.startswith("."))
    filtered_function: Callable[[List[str]], List[str]] = toolz.compose_left(
        os.listdir, curry(common_py.list_filters)(filters2), list
    )
    files: List[str] = filtered_function(folder_name)  # type: ignore

    return files


def create_folder(folder_path: str, exist_ok: bool = True) -> Either[str, Exception]:
    """
    Create a folder if it doesn't exist.

    Parameters
    ----------
    folder_path : str
        Folder path to create.
    exist_ok : bool
        Create folder if does not exist, by defaults True
    
    Returns
    -------
    Either[str, Exception]
        
        - Right(str) Success. Created folder_path.
        - Left(FileExistsError) Failure. When exist_ok is False and the folder already exists.
        - Left(Exception) Failure. Failed for another reason.

    Notes
    -----
    .. versionadded:: 0.1.0
    """
    try:
        Path(folder_path).mkdir(parents=True, exist_ok=exist_ok)
        return Right(folder_path)
    except FileExistsError as err:
        return Left(err)
    except Exception as err:
        return Left(err)
