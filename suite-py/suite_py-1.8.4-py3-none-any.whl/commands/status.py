# -*- coding: utf-8 -*-
from halo import Halo

from suite_py.lib.handler.captainhook_handler import CaptainHook
from suite_py.lib.config import Config
from suite_py.lib.logger import Logger

logger = Logger()
config = Config()

CHECKMARK = "✔"
CROSSMARK = "✘"


def entrypoint(project, timeout):
    captainhook = CaptainHook()
    if timeout:
        captainhook.set_timeout(timeout)

    with Halo(text="Contacting Captainhook...", spinner="dots", color="magenta"):
        staging_status = captainhook.status(project, "staging").json()
        production_status = captainhook.status(project, "production").json()

    forge_message(staging_status, "staging")
    forge_message(production_status, "production")


def forge_message(status, env):
    if status["locked"]:
        if status["by"] == "":
            logger.error(f"{CROSSMARK} {env}\n      lockato")
        else:
            logger.error(f"{CROSSMARK} {env}\n      lockato da {status['by']}")
    else:
        logger.info(f"{CHECKMARK} {env}\n      non lockato")
