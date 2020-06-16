"""
options.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>

>>> import namdtools
>>> namdtools.options.namd_path = '/usr/bin/namd2'
>>> namdtools.options.namd_args =

"""

import sys
this = sys.modules[__name__]

this.charmrun_path = None
this.namd_path = 'namd'

this.charmrun_args = []
this.namd_args = []
