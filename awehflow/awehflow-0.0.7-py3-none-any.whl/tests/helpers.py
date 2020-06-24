import os
import shutil

import yaml

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def tmp_dir_path():
    return os.path.join(THIS_DIR, '..', 'tmp')


def remove_dir(path):
    shutil.rmtree(path)


def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def prepare_clean_tmp_dir(folder_name=None):
    if not folder_name and os.path.exists(tmp_dir_path()):
        remove_dir(tmp_dir_path())

    ensure_dir_exists(tmp_dir_path())

    if folder_name:
        folder_path = os.path.join(tmp_dir_path(), folder_name)
        if os.path.exists(folder_path):
            remove_dir(folder_path)
        os.makedirs(folder_path)


def dict_to_yml(input_dict, path):
    with open(path, 'w') as fp:
        yaml.dump(input_dict, fp)
