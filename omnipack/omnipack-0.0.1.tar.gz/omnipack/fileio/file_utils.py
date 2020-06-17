import os
import os.path as osp
import re


def read_lines(file_path: str):
    """
    Read the file line by line
    """
    assert isinstance(file_path, str), 'file path must be a string'

    with open(file_path, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        return lines


def mkdir(workspace_path: str):
    """
    Create workspace
    """
    assert isinstance(workspace_path, str), 'workspace path must be a string'
    os.makedirs(workspace_path, exist_ok=True)


def find_files(folder_path: str, pattern: str, maxdepth: int = 1):
    """
    Read the absolute path of files under a folder
    TODO: make it recursive
    """

    assert isinstance(folder_path, str), 'folder path must be a string'
    assert maxdepth >= 0

    if maxdepth == 0:
        return []

    res = []
    for file_name in os.listdir(folder_path):

        if file_name.startswith('__') or file_name.startswith('.'):
            continue

        abs_path = osp.join(folder_path, file_name)

        if osp.isfile(abs_path):
            if re.search(pattern, file_name):
                res.append(abs_path)
        elif osp.isdir(abs_path):
            sub_list = find_files(abs_path, pattern, maxdepth-1)
            res += sub_list
    return res


def write_lines(lines, file_path: str):
    """
    Write lines into a file
    """
    assert isinstance(lines, (tuple, list))
    assert isinstance(file_path, str)

    with open(file_path, 'w') as f:
        for line in lines:
            f.write('{}\n'.format(line))
