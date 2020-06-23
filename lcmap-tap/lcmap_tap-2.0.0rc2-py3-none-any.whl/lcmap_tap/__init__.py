"""
tap - initialize/setup read only attributes
"""
import os
from pathlib import Path


def version():
    """
    Returns a string of the tap release version
    """
    return "2.0.0-rc2"


def home():
    """
    Returns a string of the working directory path
    """
    home_base_dir = str(Path.home())

    if home_base_dir.startswith("C:"):
        # If this is a local Windows file system, use the Documents directory
        work_dir = os.path.join(home_base_dir, r"Documents", r"TAP_Tool_files")
    else:
        work_dir = os.path.join(home_base_dir, r"TAP_Tool_files")

    return work_dir


def mkdirs(path):
    """
    Expects: path - a string representing a directory path
    Side effect: Creates the directory structure if it doesn't exist
    """
    if not os.path.exists(path):
        os.makedirs(path)


def top_dir():
    """
    Returns a string of the lcmap_tap package top level directory
    """
    return os.path.dirname(__file__)
