import json
import os


def get_path_testfile(filename: str) -> str:
    # absolute path to the directory of the file
    abspath_filedir = os.path.dirname(os.path.abspath(__file__))

    # folder where test files are stored
    folder_testfiles = "../../files"
    folder_testfiles = os.path.join(abspath_filedir, folder_testfiles)

    # compose filepath from dir, folder_testfiles and the filename
    return os.path.abspath("{0}/{1}".format(folder_testfiles, filename))


def get_testfile_json(filename: str) -> dict:
    # setup
    filepath = get_path_testfile(filename)

    # check that file exists
    if not os.path.exists(filepath) or not os.path.isfile(filepath):
        raise FileNotFoundError("File: {0} does not exist!".format(filepath))

    # read file and assign to global variable
    with open(filepath, "r") as file:
        # read file and load json string as dict
        return json.loads(file.read())
