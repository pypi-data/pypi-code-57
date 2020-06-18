import re

DEFAULT_VERSION = 'prod'
VALID_DAY_REGEX = re.compile(
        r'^(mon|tue|wed|thu|fri|sat|sun|today|yesterday|\d{4}-\d\d-\d\d|\d+)$', re.IGNORECASE)

TEMPLATES = [
        "CMakeLists.txt",
        "toolchain.cmake",
        "Makefile",
        "searchPath.py",
        "build.conf",
        "run",
    ]