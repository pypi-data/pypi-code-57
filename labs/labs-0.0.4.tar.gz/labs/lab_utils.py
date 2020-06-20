import os
import shutil


def clear_dir(path, filter=''):
    """
    Clear given path directories by filter condition.
    :param path: (str) the path to clear
    :param filter: (str) get directories which include the filter string in their name
    """
    # filter dirs
    dirs = [dir for dir in os.listdir(path) if filter in dir]

    # dirs paths to remove
    dirs_paths = [os.path.join(path, directory) for directory, path in list(zip(dirs, [path] * len(dirs)))]

    # remove dirs
    for dir_path in dirs_paths:
        shutil.rmtree(dir_path, ignore_errors=True)


def min_max_comparison(value, value_to_compare, condition):
    """
    Translate the values and condition to comparison operator and get result.
    :param value: (numeric) original value
    :param value_to_compare: (numeric) value to compare with, the value to beat.
    :param condition: (str) min/max condition. If "min" condition, we check whether [value] is lower or equal than
                      the value to be compared to.
    :return: bool if [value] beats [value_to_compare]
    """
    if condition == 'min':
        return value <= value_to_compare
    elif condition == 'max':
        return value >= value_to_compare
