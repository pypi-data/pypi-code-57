import os
from typing import TextIO

def listdir_fullpath(directory: str) -> list:
    """
    takes a directory path and lists out all files.
    returns file names as a list.
    """
    directory = os.path.expanduser(directory)

    file_list = []
    for file in os.listdir(directory):
        absolute_file_path = os.path.join(directory, file)
        if os.path.isfile(absolute_file_path):
            file_list.append(absolute_file_path)

    return file_list

def array_splitter(file: TextIO) -> int:
    # will refactor later; works fine for now as inline
    try:
        if file.index("~") == 0:
            file.pop(0)
            return array_splitter(file)
        else:
            return file.index("~")
    except ValueError:
        if file.index("~\n") == 0:
            file.pop(0)
            return array_splitter(file)
        else:
            return file.index("~\n")
