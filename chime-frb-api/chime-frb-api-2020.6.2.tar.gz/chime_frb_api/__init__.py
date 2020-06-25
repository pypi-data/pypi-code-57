#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pkg_resources import get_distribution as _get_distribution

# Depracated Backends
from chime_frb_api.backends import distributor
from chime_frb_api.backends import frb_master
import chime_frb_api.core

__version__ = _get_distribution("chime_frb_api").version
