from satsearch.search import Search, API_URL
from satsearch.version import __version__

import logging

# quiet loggers
logging.getLogger('urllib3').propagate = False
logging.getLogger('requests').propagate = False
