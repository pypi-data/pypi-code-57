import json
import os
import webbrowser
from typing import Text

from devyzer.constants import  DEFAULT_CONFIG_NAME


class bcolors(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def save_json_to_file(json_data, out_path):
    """
    use this function to store data in json file
    :param json_data: string of json
    :param out_path: path of file
    :return:
    """
    basedir = os.path.dirname(out_path)
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    with open(out_path, 'w') as fp:
        json.dump(json_data, fp, indent=4)


def load_json_from_file(path):
    """
    use this function to read data from json file
    :param path: path of file
    :return: content of file
    """
    with open(path) as f:
        out_data = json.load(f)
    return out_data


def wrap_with_color(text: Text, color: Text):
    return color + text + bcolors.ENDC


def print_with_color(text: Text, color: Text):
    print(wrap_with_color(text, color))


def calculate_project_url_with_access_token(url, access_token):
    """
    use for calculate git repo url with access token
    :param url: git repo url
    :param access_token: access token for user
    :return:
    """

    parts = url.split("//")
    if len(parts) == 2:
        access_part = "//x-access-token:" + access_token + "@"
        url = parts[0] + access_part + parts[1]

    return url


def get_current_configuration():
    """ return configuration in current path """

    configuration_file_dir = os.getcwd() + "/" + DEFAULT_CONFIG_NAME
    try:
        configuration = load_json_from_file(configuration_file_dir)
    except:
        configuration = None
    return configuration


def open_url(url):
    """ open browser url without printing logs or error messages to the console"""
    savout = os.dup(1)
    os.close(1)
    os.open(os.devnull, os.O_RDWR)
    try:
        webbrowser.open(url)
    finally:
        os.dup2(savout, 1)
