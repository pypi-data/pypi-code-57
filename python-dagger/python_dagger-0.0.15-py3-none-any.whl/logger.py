import logging as _logging

from dagger.config import LOG_LEVEL

# _logging.basicConfig(level=LOG_LEVEL, format='%(levelname)8s | %(filename)-30s | %(funcName)-30s | L%(lineno)-3d | %(message)s')
logger = _logging.getLogger('dagger')
