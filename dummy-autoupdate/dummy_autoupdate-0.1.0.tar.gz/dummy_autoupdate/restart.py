import os
import sys
import logging


def restart():
    logger = logging.getLogger(__name__)
    logger.info('restarting the program')
    os.execv('dummy_autoupdate', sys.argv)
