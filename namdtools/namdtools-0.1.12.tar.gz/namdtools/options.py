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

# __all__ = [
#     'charmrun_path',
#     'namd_path',
#     'charmrun_args',
#     'namd_args'
# ]

charmrun_path = None
this.charmrun_path = charmrun_path

namd_path = 'namd2'
this.namd_path = namd_path

charmrun_args = []
this.charmrun_args = charmrun_args

namd_args = []
this.namd_args = namd_args
