#  Copyright (c) 2020 Netflix.
#  All rights reserved.
import logging

import bugsnag
from bugsnag.handlers import BugsnagHandler

logger = logging.getLogger("ntscli-cloud-lib")
# for explicit use
logger.setLevel("DEBUG")
bugsnag.configure(
    api_key="5990c67cdc266249c5dd2f97eeac2447", release_stage="development", notify_release_stages=["production"], send_code=False
)


def set_logger(replacement: logging.Logger):
    """Assign this module a new shared logger."""
    global logger
    logger = replacement
    my_bugsnag = BugsnagHandler()
    my_bugsnag.setLevel(logging.ERROR)
    logger.addHandler(my_bugsnag)


# for implicit use
set_logger(logger)
