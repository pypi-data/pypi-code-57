# -*- coding: utf-8 -*-
import readline
import functools
import sys

from suite_py.lib.config import Config
from suite_py.lib.handler.youtrack_handler import YoutrackHandler
from suite_py.lib.handler.github_handler import GithubHandler
from suite_py.lib.logger import Logger
from suite_py.lib.handler import git_handler as git
from suite_py.lib.handler.captainhook_handler import CaptainHook

youtrack = YoutrackHandler()
github = GithubHandler()
logger = Logger()
config = Config()


def maybe_get_users_list(timeout):
    try:
        captainhook = CaptainHook()
        if timeout:
            captainhook.set_timeout(timeout)
        users = captainhook.get_users_list().json()
        config.put_cache("users", users)
        return users
    except Exception:
        logger.warning(
            "Non riesco ad ottenere la lista degli utenti da captainhook. Utilizzo la versione in cache."
        )
        return config.get_cache("users")


def get_pr(project):
    branch_name = git.current_branch_name(project)
    pull = github.get_pr_from_branch(project, branch_name)

    if pull.totalCount:
        pr = pull[0]
        logger.info(
            f"Ho trovato la pull request numero {pr.number} per il branch {branch_name} sul repo {project}"
        )
    else:
        logger.error(f"Nessuna pull request aperta trovata per il branch {branch_name}")
        sys.exit(-1)

    return pr


def ask_reviewer(users):
    u_completer = functools.partial(completer, users)
    readline.set_completer(u_completer)
    readline.parse_and_bind("tab: complete")

    youtrack_reviewers = []

    youtrack_reviewers = list(
        input(
            "Scegli i reviewers (nome.cognome - separati da spazio - premere TAB per autocomplete) > "
        ).split()
    )

    if not youtrack_reviewers:
        logger.warning("Devi inserire almeno un reviewer")
        return ask_reviewer(users)

    return youtrack_reviewers


def completer(users, text, state):
    options = [x["youtrack"] for x in users if text.lower() in x["youtrack"].lower()]
    try:
        return options[state]
    except IndexError:
        return None


def find_github_nicks(youtrack_reviewers, users):
    github_reviewers = []
    for rev in youtrack_reviewers:
        for user in users:
            if user["youtrack"] == rev:
                github_reviewers.append(user["github"])

    return github_reviewers


def maybe_adjust_youtrack_card(title, youtrack_reviewers):
    youtrack_id = youtrack.get_card_from_name(title)

    if youtrack_id:
        logger.info(
            f"Sposto la card {youtrack_id} in review su youtrack e aggiungo i tag degli utenti"
        )
        youtrack.update_state(youtrack_id, "Review")
        for rev in youtrack_reviewers:
            try:
                youtrack.add_tag(youtrack_id, f"review:{rev}")
            except BaseException as e:
                logger.warning(f"Non sono riuscito ad aggiungere i tag di review: {e}")
                sys.exit(-1)
    else:
        logger.warning(
            "Reviewers inseriti SOLO su GitHub. Nessuna card collegata o card nel nome del branch inesistente su YouTrack."
        )


def entrypoint(project, timeout):
    users = maybe_get_users_list(timeout)
    pr = get_pr(project)
    youtrack_reviewers = ask_reviewer(users)
    github_reviewers = find_github_nicks(youtrack_reviewers, users)
    pr.create_review_request(github_reviewers)
    logger.info("Aggiungo reviewers su GitHub")
    maybe_adjust_youtrack_card(pr.title, youtrack_reviewers)
