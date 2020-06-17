
from distutils.dir_util import copy_tree
from pathlib import Path


SKEL_PATH = Path(__file__).parents[1] / Path("skeleton")


def initialize():
    """Initialize a nbcourse directory"""
    copy_tree(SKEL_PATH, str(Path.cwd()))
