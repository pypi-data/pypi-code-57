"""
Module for OS relevant functions
"""
import os
import glob

def find_files(directory, prefix="", postfix="", recursive=True, onlyfiles=True,
          fullpath=False):
    """Clean a directory based on files in directory

    Parameters
    ----------
    directory : str
        Directory to search in
    prefix : str (optional)
        Only remove files with this prefix
    postfix : str (optional)
        Only remove files with the postfix
    recursive : Boolean (optional)
        Go into directories recursively. Defaults to True
    onlyfiles : Boolean (optional)
        Show only files. Defaults to True
    fullpath : Boolean (optional)
        Give full path. Defaults to False. If recursive=True, fullpath is given automatically.

    Returns
    -------
    files : list
        List containing file names that matches criterias

    Notes
    -----
    files = find_files('/some/path/', prefix="", postfix=".nc", recursive=False,
               onlyfiles=True, fullpath=False)
    """

    if recursive:    
        fullpath = False
        files = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(directory):
            for file in f:
                if file.startswith(prefix) and file.endswith(postfix):
                    files.append(os.path.join(r, file))

    elif not recursive:

        if onlyfiles:
            files = [f for f in os.listdir(directory) if
                     f.endswith(postfix) and f.startswith(prefix) and
                     os.path.isfile(directory+f)]

        elif not onlyfiles:
            files = [f for f in os.listdir(directory) if
                     f.endswith(postfix) and f.startswith(prefix)]

    if fullpath:
        files = [directory+f for f in files]

    return files
