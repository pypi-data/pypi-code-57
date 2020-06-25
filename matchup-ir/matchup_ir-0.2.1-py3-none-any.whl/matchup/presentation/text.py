"""
    Module that has two important structures used throughout the library: Term and Line
"""

from collections import namedtuple

Term = namedtuple("Term", "word position")
Line = namedtuple("Line", "content number")
