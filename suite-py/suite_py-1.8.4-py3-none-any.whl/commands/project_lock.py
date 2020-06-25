# -*- coding: utf-8 -*-
import sys
import requests

from suite_py.lib.handler.captainhook_handler import CaptainHook
from suite_py.lib.logger import Logger

logger = Logger()


def entrypoint(project, timeout, env, action):
    captainhook = CaptainHook()
    if timeout:
        captainhook.set_timeout(timeout)
    env = parse_env(env)
    if action == "lock":
        try:
            req = captainhook.lock_project(project, env)
            handle_request(req)
            logger.info(f"Bloccato deploy su {env} del progetto {project}")
        except requests.exceptions.Timeout:
            logger.warning(
                "Richiesta a Captainhook in timeout. Prova con suite-py --timeout=60 lock-project lock"
            )
            sys.exit(1)
    elif action == "unlock":
        try:
            req = captainhook.unlock_project(project, env)
            handle_request(req)
            logger.info(f"Abilitato deploy su {env} del progetto {project}")
        except requests.exceptions.Timeout:
            logger.warning(
                "Richiesta a Captainhook in timeout. Prova con suite-py --timeout=60 lock-project unlock"
            )
            sys.exit(1)
    else:
        logger.warning("Non ho capito che cosa devo fare")
        sys.exit(-1)


def handle_request(request):
    if request.status_code != 200:
        logger.error(
            "Qualcosa è andato storto durante la richiesta. Richiedi supporto ai devops su slack."
        )
        sys.exit(-1)

    return True


def parse_env(env):
    # implementare uno switch era troppo noioso
    if env == "deploy":
        return "production"
    if env == "merge":
        return "staging"
    return env
