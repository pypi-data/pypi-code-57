# -*- coding: utf-8 -*-
"""Webscraper for Czechia COVID19 data.
 
Sources:
    * https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19
    * ...
Todo:
    * More sources
    * Caching
"""

# ===== members =====
from .mzcr import *
# ===================

import pkg_resources

try:
    __version__ = pkg_resources.get_distribution("covid19czechia").version
except:
    __version__ = None