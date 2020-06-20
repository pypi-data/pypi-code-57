# -*- coding: utf-8 -*-
"""Webscraper for Eurostat.
 
Archive URL: https://ec.europa.eu/eurostat
Todo:
    * caching
"""

import pkg_resources
from .deaths import *
from .populations import *
from .cache import *

try:
    __version__ = pkg_resources.get_distribution("eurostat_deaths").version
except:
    __version__ = None