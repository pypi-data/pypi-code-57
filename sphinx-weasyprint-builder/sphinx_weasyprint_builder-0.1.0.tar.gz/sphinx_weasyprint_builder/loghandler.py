#!/usr/bin/env python3

import logging
from sphinx.util import logging as sphinx_logging


logger = sphinx_logging.getLogger('weasyprint_builder')


def init_wpsphinx_log():
    """
    Initialize logging for WeasyPrint.
    """
    wplogger = logging.getLogger('weasyprint')
    wphandler = SphinxWPHandler()
    wphandler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    wphandler.setFormatter(formatter)
    wplogger.addHandler(wphandler)


class SphinxWPHandler(logging.StreamHandler):
    """
    Resend WeasyPrint logging to Sphinx output.
    """
    def __init__(self):
        super(SphinxWPHandler, self).__init__()

    def emit(self, record):
        logger.handle(record)
