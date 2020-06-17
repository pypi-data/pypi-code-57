""" __INIT__ module needed now that the EVC_Manager runs as a
Python module. """

import logging
from logging import NullHandler
from .evc_manager import EvcManager
from .libs.core.prep_cli import get_cli
from .libs.core.log import info

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(NullHandler())
