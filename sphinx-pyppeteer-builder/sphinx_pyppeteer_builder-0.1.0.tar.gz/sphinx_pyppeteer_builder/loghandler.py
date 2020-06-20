#!/usr/bin/env python3

import logging
from sphinx.util import logging as sphinx_logging

logger = sphinx_logging.getLogger('pyppeteer')
ppsphinx_log_inited = False


def init_ppsphinx_log() -> None:
    """
    Initialize logging for Pyppeteer.
    """
    if ppsphinx_log_inited:
        return

    formatter = logging.Formatter('%(message)s')
    pphandler = SphinxPyppeteerHandler()
    pphandler.setLevel(logging.DEBUG)
    pphandler.setFormatter(formatter)
    logger_names = (
        'pyppeteer',
        'pyppeteer.browser',
        'pyppeteer.chromium_downloader',
        'pyppeteer.command',
        'pyppeteer.connection',
        'pyppeteer.coverage',
        'pyppeteer.element_handle',
        'pyppeteer.execution_context',
        'pyppeteer.frame_manager',
        'pyppeteer.helper',
        'pyppeteer.launcher',
        'pyppeteer.navigator_watcher',
        'pyppeteer.network_manager',
        'pyppeteer.page',
        'pyppeteer.worker',
    )
    for logger_name in logger_names:
        pplogger = logging.getLogger(logger_name)
        pplogger.addHandler(pphandler)


class SphinxPyppeteerHandler(logging.StreamHandler):
    """
    Resend Pyppeteer logging to Sphinx output.
    """
    def __init__(self):
        super(SphinxPyppeteerHandler, self).__init__()

    def emit(self, record):
        logger.handle(record)
