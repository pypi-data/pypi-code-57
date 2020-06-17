#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Utils functions.

This module is a groups for extra utils functions used
in other packages or modules.
"""

import os
import csv


def sanitize_path(path, basedir=None):
    """Sanitize file path.

    Clean the string path of file. Expands environment variables,
    relative paths and symbols. `Note` : It does not check whether
    the path exists.

    :param path: The string representing a path to be sanitized.
    :type path: str
    :rtype: str
    :returns: An absolute path of the file.
    """

    if basedir is None:
        basedir = os.getcwd()
    elif os.path.isfile(basedir):
        basedir = os.path.dirname(basedir)

    final_path = os.path.expanduser(os.path.expandvars(path))
    final_path = os.path.join(basedir, final_path)

    return os.path.normpath(final_path)

def load_csv(path, delimiter=','):
    """Load csv data from file.

    This function read csv file and uses first line as header and returns
    a list of dict object.

    :param path: The string representing a path of csv file.
    :type path: str
    :rtype: list
    :returns: List of dict object.
    :raises FileNotFoundError: if the path of file does not exist.
    """

    csv_path = sanitize_path(path)
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"File not found: '{csv_path}'")

    # load data
    with open(csv_path, 'rt') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        data = [dict(row) for row in reader]

    return data

def find_template_dir():
    """Template dir finder.

    Search for a directory named ``templates``. The first found is used.
    Loading order:

    * environment variable: $PYTH_CONFIG_DIR/templates
    * working directory: $CWD/templates
    * home directory: $HOME/.pyth/templates
    * system default: /etc/pyth/templates

    :rtype: str
    :return: The first path found for the template base dir.
    """

    potential_paths = []

    # Environment path
    path_from_env = os.getenv("PYTH_CONFIG_DIR")
    if path_from_env:
        path_from_env = sanitize_path(path_from_env)
        potential_paths.append(os.path.join(path_from_env, "templates"))

    # Templates in current working directory
    path_from_cwd = os.path.join(os.getcwd(), "templates")
    potential_paths.append(path_from_cwd)

    # Home user directory
    potential_paths.append(sanitize_path("~/.pyth/templates"))

    # System default templates
    potential_paths.append("/etc/pyth/templates")

    for path in potential_paths:
        if os.path.exists(path):
            break
    else:
        path = None

    return path
