__version__ = "6.0.25"

import logging

from zuper_commons.logs.col_logging import setup_logging

# noinspection PyUnresolvedReferences
from zuper_ipce import __version__ as _v

logging.basicConfig()
setup_logging()
logger = logging.getLogger("zuper-nodes")
logger.setLevel(logging.DEBUG)
logger.info(f"zuper-nodes {__version__}")

from .language import *

from .language_parse import *
from .language_recognize import *

from .structures import *
from .compatibility import *
