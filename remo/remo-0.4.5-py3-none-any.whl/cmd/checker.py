import os
import shutil

from .log import Log
from .postgres import get_instance
from remo_app.config import REMO_HOME


def is_tool_exists(tool):
    return bool(shutil.which(tool))


def check_runtime_requirements(db_params):
    if not db_params:
        Log.exit("Invalid database connection parameters.")

    get_instance().on_start_check(db_params)

    # TODO: this needed only for Windows
    vips_bin_path = str(os.path.join(REMO_HOME, 'libs', 'vips', 'vips-dev-8.8', 'bin'))
    if os.path.exists(vips_bin_path) and vips_bin_path not in os.environ["PATH"]:
        os.environ["PATH"] = vips_bin_path + os.pathsep + os.environ["PATH"]

    vips = is_tool_exists('vips')
    if vips:
        return

    msg = 'Remo stopped as some requirements are missing:'
    if not vips:
        msg = f"""{msg}

vips library was not found.
Please do `python -m remo_app init` or install library manually."""

    Log.exit_warn(msg)


def check_installation_requirements():
    sqlite = is_tool_exists('sqlite3')
    if all((sqlite,)):
        return

    msg = 'Remo stopped as some requirements are missing:'

    if not sqlite:
        msg = f"""{msg}

SQLite binaries not installed.
You can install remo in a conda environment, which comes with SQLite pre-installed.
Or can install SQLite manually,
e.g. see instructions here https://www.sqlitetutorial.net/download-install-sqlite/"""

    Log.exit_warn(msg)
