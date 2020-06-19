import sys

LOOKUP_DIR = "lookup"

# linux, win32, cygwin, darwin
IS_WINDOWS = sys.platform.lower().startswith("win")
IS_LINUX = sys.platform.lower().startswith("linux")
EXECUTABLE_EXTENSION = ".exe" if IS_WINDOWS else ".out"
TMP_EXECUTABLE = "tmp.exe" if IS_WINDOWS else "tmp.out"
COMPILED_O = "cmp.o"
TMP_O = "tmp.o"
COMPILER = "g++" if IS_WINDOWS or IS_LINUX else "g++-9"

JSON_HPP = "json.hpp"
CPP_EVAL_UTIL_CPP = "cpp_eval_util.cpp"
CPP_EVAL_UTIL_H = "cpp_eval_util.h"
EMPTY_MAIN = "empty_main.cpp"
CPP_EVAL_UTIL_O = "cpp_eval_util.o"

PY_RUNNER = "python" if IS_WINDOWS else "python3"

FAIL = "fail"
PASS = "pass"

WATCHDOG_TIMEOUT = 600
RUNNER_USER = "runner"

EXECUTABLE_TIMEOUT = 30  # seconds
MAX_VIRTUAL_MEMORY = 256 * 1024 * 1024 # 256 MB