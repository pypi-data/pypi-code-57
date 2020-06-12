"""
cache.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

import sys


# Reference to this module
this = sys.modules[__name__]

# Cache to store data in session
this.cache = []
