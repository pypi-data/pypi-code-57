# coding: utf8
"""
Reads lines from a plaintext file, separated by categories.

Category names are delimited by square brackets as the first and last
characters of the line.

Items in each category are just plain text, one item per line

Any lines before the first category will be assigned to 'uncategorized'

The format is simmilar to .ini files, only you don't have thei 'key'='value'
structure in the items.

Blank lines and lines that begin with '#' are ignored.

Example of a file:
------------------

# the following lines will be assigned to 'uncategorized`

Linux
Windows
MacOS

[Directories]
/home
/usr
/etc

# this line will be ignored

[Files]
README.md
module.py
"""


__title__ = "categorylist"
__version__ = "0.1.0"
__license__ = "GNU General Public License v2 or later (GPLv2+)"
__author__ = "Bento Loewenstein"

from .catlist import catlist
