# -*- coding: utf-8 -*-
import sys

from halo import Halo

from suite_py.lib.handler.youtrack_handler import YoutrackHandler
from suite_py.lib.handler.github_handler import GithubHandler
from suite_py.lib.handler.captainhook_handler import CaptainHook
from suite_py.lib.config import Config
from suite_py.lib.logger import Logger
from suite_py.lib.handler import prompt_utils
from suite_py.lib.qainit import qainit_shutdown
from suite_py.lib.handler import git_handler as git
from suite_py.lib.handler import drone_handler as drone


youtrack = YoutrackHandler()
github = GithubHandler()
logger = Logger()
config = Config()

CHECKMARK = "✔"
CROSSMARK = "✘"


def entrypoint(project, timeout):
    captainhook = CaptainHook()
    if timeout:
        captainhook.set_timeout(timeout)

    stop_if_master_locked(project, captainhook)

    pr = select_pr(project)

    print(f"\nHai selezionato: \n{check_pr_status(project, pr)}")
    if not prompt_utils.ask_confirm("Vuoi continuare il merge?", default=False):
        sys.exit(0)

    branch_name = pr.head.ref
    youtrack_id = youtrack.get_card_from_name(branch_name)

    check_migrations_merge(pr)

    logger.info("Eseguo il merge...")

    merge_status = pr.merge(
        commit_title=f"{pr.title} (#{pr.number})",
        commit_message="",
        merge_method="squash",
    )

    if not merge_status.merged:
        logger.error("Si è verificato un errore durante il merge.")
        sys.exit(-1)

    drone_build_number = drone.get_pr_build_number(project, merge_status.sha)
    drone_build_url = drone.get_build_url(project, drone_build_number)

    if drone_build_url:
        logger.info(
            f"Pull request mergiata su master! Puoi seguire lo stato della build su {drone_build_url}"
        )
    else:
        logger.info("Pull request mergiata su master!")

    git.fetch(project)
    if git.remote_branch_exists(project, branch_name):
        git.delete_remote_branch(project, branch_name)

    if prompt_utils.ask_confirm(
        "Vuoi bloccare staging? (Necessario se bisogna testare su staging)",
        default=False,
    ):
        if drone.prestart_success(project, drone_build_number):
            captainhook.lock_project(project, "staging")
        else:
            logger.error(
                "Problemi con la build su drone, non riesco a bloccare staging"
            )
            sys.exit(-1)

    if youtrack_id:
        logger.info("Aggiorno lo stato della card su youtrack...")
        youtrack.update_state(youtrack_id, config.load()["youtrack"]["merged_state"])
        logger.info("Card aggiornata")

        logger.info("Spengo il qa, se esiste")
        qainit_shutdown(youtrack_id)
    else:
        logger.warning(
            "Non sono riuscito a trovare una issue YouTrack nel nome del branch o la issue indicata non esiste."
        )
        logger.warning(
            "Nessuna card aggiornata su YouTrack e nessun QA spento in automatico"
        )

    logger.info("Tutto fatto!")
    sys.exit()


def select_pr(project):
    if github.user_is_admin(project):
        logger.warning(
            "Sei admin del repository, puoi fare il merge skippando i check (CI, review, ecc...)\nDa grandi poteri derivano grandi responsabilita'"
        )

    with Halo(text="Loading pull requests...", spinner="dots", color="magenta"):
        choices = [
            {"name": pr.title, "value": pr} for pr in github.get_list_pr(project)
        ]
    if choices:
        choices.sort(key=lambda x: x["name"])
        return prompt_utils.ask_choices("Seleziona PR: ", choices)

    logger.error(
        f"Non esistono pull request pronte per il merge o potresti non avere i permessi, per favore controlla su https://github.com/primait/{project}/pulls"
    )
    sys.exit(-1)


def stop_if_master_locked(project, captainhook):
    request = captainhook.status(project, "staging")

    if request.status_code != 200:
        logger.error("Impossibile determinare lo stato del lock su master.")
        sys.exit(-1)

    request_object = request.json()
    if request_object["locked"]:
        logger.error(
            f"Il progetto è lockato su staging da {request_object['by']}. Impossibile continuare."
        )
        sys.exit(-1)


def check_migrations_merge(pr):
    files_changed = [x.filename for x in pr.get_files()]
    if git.migrations_found(files_changed):
        logger.warning("ATTENZIONE: migrations rilevate nel codice")
        if not prompt_utils.ask_confirm("Sicuro di voler continuare?"):
            sys.exit(-1)


def check_pr_status(project, pr):
    build_status = CHECKMARK
    reviews = CHECKMARK
    if pr.mergeable_state == "blocked":
        build_status = pr_build_status(project, pr)
        reviews = pr_reviews(pr)

    return f"#{pr.number} {pr.title}\n     build: {build_status} - reviews: {reviews}\n"


def pr_build_status(project, pr):
    if github.get_build_status(project, pr.head.sha).state == "success":
        return CHECKMARK
    return CROSSMARK


def pr_reviews(pr):
    reviews = [r for r in pr.get_reviews() if r.state == "APPROVED"]
    if reviews:
        return CHECKMARK
    return CROSSMARK
