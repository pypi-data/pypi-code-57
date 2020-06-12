"""
Python logging, configured the way I like it.
"""

from . import _bootstrap  # for side effects

from .utils import get_logger, get_file_logger, use_utc, use_clock
from .handlers import enable_stderr, disable_stderr, enable_file
from .level import set_log_level_override
from .logger import prefixed


_bootstrap, get_logger, get_file_logger, use_utc, use_clock  # pyflakes
set_log_level_override, prefixed, enable_stderr, disable_stderr, enable_file  # pyflakes
