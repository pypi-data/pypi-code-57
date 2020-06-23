"""
Module for OS relevant functions
"""
import os
import time
import glob

def find_files(directory, prefix="", postfix="", recursive=True, onlyfiles=True,
          fullpath=False, olderthan=None):
    """Find files in a directory.

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
    olderthan : int (optional)
        Match only files older than X seconds from now. Defaults to None

    Returns
    -------
    files : list
        List containing file names that matches criterias

    Notes
    -----
    files = find_files('/foo/', prefix="", postfix="", recursive=False,
               onlyfiles=True, fullpath=True, olderthan=86400*100)
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

    if olderthan is not None:
        now = time.time()
        tfiles = []
        for f in files:
            if not fullpath:
                if os.path.getmtime(os.path.join(directory, f)) < (now - olderthan):
                    tfiles.append(f)
            else:
                if os.path.getmtime(f) < (now - olderthan):
                    tfiles.append(f)
        files = tfiles

    return files


def clean(files):
    """Removes files from the system.
    Note that filenames must be given as full paths

    Parameters
    ----------
    files : list
        List of files to remove.
    """
    for f in files:
        try:
            os.remove(f)
        except OSError:
            pass
    return
