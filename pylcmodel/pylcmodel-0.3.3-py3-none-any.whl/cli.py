from . import _lcmodel
from . import namelist

import os
import sys


def find_config():
    """
    Searches for the .pylcmodel config file, first in the current directory and
    then in the user's home folder. Raises a FileNotFoundError if the config
    file is not present in either location.

    Returns
    -------
    config: str
        The path to a .pylcmodel config file
    """
    print("in find_config()")
    print(os.getcwd())
    print(os.listdir(os.getcwd()))
    print(os.path.expanduser("~/.pylcmodel"))
    if os.path.isfile(os.path.join(os.getcwd(), ".pylcmodel")):
        return os.path.join(os.getcwd(), ".pylcmodel")
    elif os.path.isfile(os.path.expanduser("~/.pylcmodel")):
        return os.path.expanduser("~/.pylcmodel")
    else:
        raise FileNotFoundError("No .pylcmodel config file found.")


def read_config(config_file):
    """
    Load configuration parameters from the supplied file path. The file should
    contain one parameter on each line with the format `key=value`. Lines
    starting with a # are ignored

    Parameters
    ----------
    config_file: dict
        A dictionary with the necessary parameters to run pylcmodel
    :return:
    """
    config_dict = {
        "port": "22",
        "persist_remote_files": False
    }
    with open(config_file) as fin:
        for config_line in fin:
            config_line = config_line.strip()
            # check for commented out lines
            if config_line.startswith("#") or len(config_line) == 0:
                continue
            key, value = config_line.split("=")
            config_dict[key.rstrip()] = value.lstrip()

    return config_dict


def lcmodel_cli():
    print("running lcmodel remotely 1")

    config_path = find_config()
    config_dict = read_config(config_path)

    control_string = sys.stdin.read()
    print(control_string)
    print("parsing namelist")
    control = namelist.reads(control_string.strip())[1]

    print(control)

    return _lcmodel.run_lcm_remote(config_dict, control)

