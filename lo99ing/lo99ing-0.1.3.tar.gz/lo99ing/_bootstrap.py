"""
perform bootstrapping (at import time) required by the lo99ing package.
"""

import logging
from .logger import Lo99er
from .handlers import enable_stderr
from .level import log_level_manager, set_log_level

################################################################################

# Use our own custom logger class:
logging.setLoggerClass(Lo99er)

# Add the default handler to root logger:
enable_stderr(logging.root)

################################################################################
# log levels

# Every Lo99er sets its own level, so the root logger is set to be promiscuous:
logging.root.setLevel(logging.NOTSET)

# but we also need to set default level on loggers which has been created before
# importing lo99ing
for logger_name, logger in logging.Logger.manager.loggerDict.items():
    if logger == logging.root or getattr(logger, 'level', object()) != logging.NOTSET:
        continue
    log_level_manager.set_initial(logger_name, logging.WARNING)
    set_log_level(logger_name, log_level_manager.get_effective(logger_name))


################################################################################
