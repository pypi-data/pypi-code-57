"""
__init__.py
Contains the package name and the author's name
---
get_author() returns the author
mouse creates the mouse Class
"""


import numpy
import scipy
import random
import pyautogui

from scipy import interpolate

from .mouse import Mouse


name = 'pyHM'
author = "Joe Tilsed - https://linkedin.com/in/joetilsed/"


def get_author():
    return author


mouse_dependencies = {
    'interpolate': interpolate,
    'pyautogui': pyautogui,
    'numpy': numpy,
    'random': random,
    'scipy': scipy
}
mouse = Mouse(mouse_dependencies)


# That's all folks...
