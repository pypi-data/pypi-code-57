from pathlib import Path
import os
import sys
from . import IO
import functools
import json

def getSSP_(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		cwd = os.getcwd()
		filepath = os.path.dirname(os.path.abspath(__file__))
		os.chdir(filepath)
		os.chdir("../motion/settings/SSP")
		return func(*args, **kwargs)
		os.chdir(cwd)
	return wrapper

@getSSP_
def getSSP(file_name):
    a = open("{}.json".format(file_name))
    b = json.load(a)
    return b

p = os.path.dirname(__file__)
if "Anaconda3" in p:
    ssp = getSSP("SSP")
    try:
        homedir = Path.home() / ssp["data_path"]
    except KeyError:
        pass
else:
    homedir = Path(p).joinpath("..","_MeasurementData")




def home():
    """Summary line.
    List the directories and files contained in the data directory.
    
    Parameters
    ----------
    None

    Returns
    -------
    directories and files
    """
    d, f = [], []
    for i in homedir.iterdir():
        if i.is_dir():
            d.append(i)
        elif i.is_file():
            f.append(i)
    print("The home directory of measurement data has been searched.")
    print("The following directories and files were found : ")
    print("")
    print("---------------")
    print("  Directoris ")
    print("---------------")
    if d:
        for i in d:
            print("    {}".format(i.name))
    else:
        print("    The directory could not be found.")
    print("---------------")
    print("  Files ")
    print("---------------")
    if f:
        for i in f:
            print("    {}".format(i.name))
    else:
        print("    The file could not be found")
    print("")
    print("- {} directories".format(len(d)))
    print("- {} files".format(len(f)))

def home_isdir():
    """Summary line.
    List the directories contained in the data directory.
    
    Parameters
    ----------
    None

    Returns
    -------
    directories
    """
    d = []
    for i in homedir.iterdir():
        if i.is_dir():
            d.append(i)
    print("The home directory of measurement data has been searched.")
    print("The following directories were found : ")
    print("")
    print("---------------")
    print("  Directoris ")
    print("---------------")
    if d:
        for i in d:
            print("    {}".format(i.name))
    else:
        print("    The directory could not be found.")
    print("")
    print("- {} directories".format(len(d)))

def home_isfile(extension="pkl"):
    """Summary line.
    List the files name contained in the data directory.
    In order to enumerate regardless of the extension, set extension = "*".
    
    Parameters
    ----------
    None

    Returns
    -------
    files name
    """
    f = []
    for i in homedir.glob("*.{}".format(extension)):
        if i.is_file():
            f.append(i)
    print("The home directory of measurement data has been searched.")
    print("The following directories were found : ")
    print("")
    print("---------------")
    print("  Files ")
    print("---------------")
    if f:
        for i in f:
            print("    {}".format(i.name))
    else:
        print("    The file could not be found.")
    print("")
    print("- {} files".format(len(f)))

def dd_isdir(*path):
    """Summary line.
    List all the directories contained in the specified directory.
    
    Parameters
    ----------
    path : str
        variable-length argument

    Returns
    -------
    directory name
    """
    p = homedir.joinpath(*path)
    d = []
    try:
        for i in p.iterdir():
            if i.is_dir():
                d.append(i)
        print("The following directories were searched :")
        hoge = ""
        for i in path:
            hoge += "/" + i
        print("    _MeasurementData{}".format(hoge))
        print("")
        print("The following directories were found : ")
        print("---------------")
        print("  Directoris ")
        print("---------------")
        if d:
            for i in d:
                print("    {}".format(i.name))
        else:
            print("    The directory could not be found.")
        print("")
        print("- {} directories".format(len(d)))
    except FileNotFoundError:
        print("The directory does not exist. Please check the directory again.")
        print("---------------------------------------------------------------")
        print("The directory you specified is :")
        print("    _MeasurementData/{}".format(*path))

def dd_isfile(*path,extension="pkl"):
    """Summary line.
    List all the files contained in the specified directory.
    In order to enumerate regardless of the extension, set extension = "*".

    Parameters
    ----------
    path : str
        variable-length argument

    Returns
    -------
    directory name
    """
    p = homedir.joinpath(*path)
    f = []
    try:
        for i in p.glob("*.{}".format(extension)):
            f.append(i)
        print("The following files were searched :")
        hoge = ""
        for i in path:
            hoge += "/" + i
        print("    _MeasurementData{}".format(hoge))
        print("")
        print("The following files were found : ")
        print("---------------")
        print("  Files ")
        print("---------------")
        if f:
            for i in f:
                print("    {}".format(i.name))
        else:
            print("    The directory could not be found.")
        print("")
        print("- {} files".format(len(f)))
    except FileNotFoundError:
        print("The directory does not exist. Please check the directory again.")
        print("---------------------------------------------------------------")
        print("The directory you specified is :")
        print("    _MeasurementData/{}".format(*path))

def dd_all(*path):
    """Summary line.
    List the directories and files contained the specified directory.

    Parameters
    ----------
    path : str
        variable-length argument

    Returns
    -------
    directories and files
    """

    p = homedir.joinpath(*path)

        
    d, f = [], []
    try:
        for i in p.iterdir():
            if i.is_dir():
                d.append(i)
            else:
                f.append(i)
        print("The following directories were searched :")
        hoge = ""
        for i in path:
            hoge += "/" + i
        print("    _MeasurementData{}".format(hoge))
        print("")
        print("---------------")
        print("  Directoris ")
        print("---------------")
        if d:
            for i in d:
                print("    {}".format(i.name))
        else:
            print("    The directories could not be found.")
        print("---------------")
        print("  Files ")
        print("---------------")
        if f:
            for i in f:
                print("    {}".format(i.name))
        else:
            print("    The file could not be found.")
        print("")
        print("- {} directories".format(len(d)))
        print("- {} files".format(len(f)))
        
    except FileNotFoundError:
        print("The directory does not exist. Please check the directory again.")
        print("---------------------------------------------------------------")
        print("The directory you specified is :")
        print("    _MeasurementData/{}".format(*path))


def file_out(*path, extension="pkl"):
    """Summary line.
    Output files in a specific directory as a list.
    path (variable-length argument), extension = "pkl" (default).
    In order to output regardless of the extension, set extension = "*".

    Parameters
    ----------
    path : str
        variable-length argument
    extension : str
        default is "pkl", "*" is all files.

    Returns
    -------
    list.
    """
    p = homedir.joinpath(*path)
    f = []
    try:
        for i in p.glob("*.{}".format(extension)):
            f.append(i.name)
        if f:
            return f
        else:
            print("    The directory could not be found.")
        print("")
        print("- {} files".format(len(f)))
    except FileNotFoundError:
        print("The directory does not exist. Please check the directory again.")
        print("---------------------------------------------------------------")
        print("The directory you specified is :")
        print("    _MeasurementData/{}".format(*path))

def absfile_out(*path, extension="pkl"):
    """Summary line.
    Output files in a specific directory as a list.
    path (variable-length argument), extension = "pkl" (default).
    In order to output regardless of the extension, set extension = "*".

    Parameters
    ----------
    path : str
        variable-length argument
    extension : str
        default is "pkl", "*" is all files.

    Returns
    -------
    list.
    """
    p = homedir.joinpath(*path)
    f = []
    try:
        for i in p.glob("*.{}".format(extension)):
            f.append(i.resolve())
        if f:
            return f
        else:
            print("    The directory could not be found.")
        print("")
        print("- {} files".format(len(f)))
    except FileNotFoundError:
        print("The directory does not exist. Please check the directory again.")
        print("---------------------------------------------------------------")
        print("The directory you specified is :")
        print("    _MeasurementData/{}".format(*path))