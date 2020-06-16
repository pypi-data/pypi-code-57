"""
The `temporython` library functions.
"""

__all__ = ['process_files_in_argv', 'process_files', 'LIBRARY_PATH', 'main']

import os

LIBRARY_PATH = os.path.dirname(os.path.realpath(__file__))
from .temporython_inline_process_files_library import process_files_in_argv, process_files, main
from .temporython_inline_process_pipe_library import pipe_main
