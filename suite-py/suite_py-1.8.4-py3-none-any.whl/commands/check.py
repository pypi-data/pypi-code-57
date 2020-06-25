# -*- coding: utf-8 -*-

from suite_py.lib.handler.captainhook_handler import CaptainHook
from suite_py.lib.handler.github_handler import GithubHandler
from suite_py.lib.handler.youtrack_handler import YoutrackHandler
from suite_py.lib.handler import drone_handler as drone
from suite_py.lib.handler import prompt_utils
from suite_py.lib.tokens import Tokens
from suite_py.lib.config import Config
from suite_py.lib.logger import Logger

logger = Logger()
config = Config()
tokens = Tokens()
youtrack = YoutrackHandler()
github = GithubHandler()
captainhook = CaptainHook()

CHECKMARK = "✔"
CROSSMARK = "✘"
INVALID_OR_MISSING_TOKEN = []


def entrypoint(timeout):
    if timeout:
        captainhook.set_timeout(timeout)

    # Services
    github_status = check_github()
    drone_status = check_drone()
    youtrack_status = check_youtrack()
    captainhook_status = check_captainhook()

    forge_message("Github", github_status)
    forge_message("Drone", drone_status)
    forge_message("Youtrack", youtrack_status)
    forge_message("Captainhook", captainhook_status)

    # Tokens
    if len(INVALID_OR_MISSING_TOKEN) > 0 and prompt_utils.ask_confirm(
        "Vuoi reinserire i token mancanti?", default=True
    ):
        reiterate_token()


def check_github():
    if tokens.github:
        try:
            if github.get_user().login:
                return "ok"
            INVALID_OR_MISSING_TOKEN.append("github")
            return "invalid_token"
        except Exception:
            INVALID_OR_MISSING_TOKEN.append("github")
            return "invalid_token"
    else:
        INVALID_OR_MISSING_TOKEN.append("github")
        return "missing_token"


def check_drone():
    if tokens.drone:
        try:
            drone_user = drone.get_user()
            if "message" in drone_user and drone_user["message"] == "Unauthorized":
                INVALID_OR_MISSING_TOKEN.append("drone")
                return "invalid_token"
            return "ok"
        except Exception:
            INVALID_OR_MISSING_TOKEN.append("drone")
            return "invalid_token"
    else:
        INVALID_OR_MISSING_TOKEN.append("drone")
        return "missing_token"


def check_youtrack():
    if tokens.youtrack:
        try:
            youtrack.get_projects()
            return "ok"
        except Exception:
            INVALID_OR_MISSING_TOKEN.append("youtrack")
            return "invalid_token"
    else:
        INVALID_OR_MISSING_TOKEN.append("youtrack")
        return "missing_token"


def check_captainhook():
    try:
        if captainhook.check().status_code != 200:
            return "unreachable"
        return "ok"
    except Exception:
        return "unreachable"


def forge_message(service, result):
    cases = {
        "ok": f"{service:>12}:{CHECKMARK:>12} ok",
        "invalid_token": f"{service:>12}:{CROSSMARK:>12} token non valido",
        "missing_token": f"{service:>12}:{CROSSMARK:>12} token mancante",
        "unreachable": f"{service:>12}:{CROSSMARK:>12} non raggiungibile",
    }
    print(cases.get(result, f"{service}: stato sconosciuto"))


def reiterate_token():
    for service in INVALID_OR_MISSING_TOKEN:
        new_token = prompt_utils.ask_questions_input(
            f"Inserisci nuovo token per {service}: "
        )
        tokens.edit(service, new_token)

    logger.info("Salvo i nuovi token...")
    tokens.save()
    logger.info(f"{CHECKMARK} Fatto!")
