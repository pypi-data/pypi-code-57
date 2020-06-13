__author__ = """Arkadiusz Michał Ryś"""
__email__ = "Arkadiusz.Michal.Rys@gmail.com"
__version__ = "0.4.0"

from arklog.logging import (
    CRITICAL,
    ERROR,
    WARNING,
    INFO,
    EXTRA,
    DEBUG,
    NOTSET,

    ColorFormatter,
    create_logger,
    set_defaults,
    set_from_file,
    log,
    success,
    extra,
)

from logging import (
    debug,
    info,
    warning,
    error,
    critical,
    exception,
)
