import os

from yqn_common.str_util import ends_with


def get_absolute_path(p):
    if p.startswith('~'):
        p = os.path.expanduser(p)
    return os.path.abspath(p)


def ls(path='.', suffix=None):
    path = get_absolute_path(path)
    files = os.listdir(path)

    if suffix is None:
        return files

    filtered = []
    for f in files:
        if ends_with(f, suffix, ignore_case=True):
            filtered.append(f)

    return filtered
