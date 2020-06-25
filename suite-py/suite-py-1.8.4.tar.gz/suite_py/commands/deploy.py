# -*- coding: utf-8 -*-
import sys
import semver

from halo import Halo

from suite_py.lib.handler.youtrack_handler import YoutrackHandler
from suite_py.lib.handler.github_handler import GithubHandler
from suite_py.lib.handler.captainhook_handler import CaptainHook
from suite_py.lib.handler import prompt_utils
from suite_py.lib.handler import git_handler as git
from suite_py.lib.handler import drone_handler as drone
from suite_py.lib.logger import Logger
from suite_py.lib.config import Config


youtrack = YoutrackHandler()
github = GithubHandler()
config = Config()
logger = Logger()


def entrypoint(project, timeout):

    lock = CaptainHook()
    if timeout:
        lock.set_timeout(timeout)
    stop_if_prod_locked(project, lock)

    git.fetch(project)
    repo = github.get_repo(project)

    latest_release = get_release(repo)

    versions = bump_versions(latest_release.title)

    commits = github.get_commits_since_release(repo, latest_release)

    check_migrations_deploy(commits)

    message = "\n".join(["* " + c.commit.message.splitlines()[0] for c in commits])

    logger.info(f"\nLista dei commit:\n{message}\n")

    if not prompt_utils.ask_confirm("Vuoi continuare?"):
        sys.exit(-1)

    new_version = prompt_utils.ask_choices(
        "Seleziona versione:",
        [
            {"name": f"Patch {versions['patch']}", "value": versions["patch"]},
            {"name": f"Minor {versions['minor']}", "value": versions["minor"]},
            {"name": f"Major {versions['major']}", "value": versions["major"]},
        ],
    )

    release_state = config.load()["youtrack"]["release_state"]

    issue_ids = youtrack.get_issue_ids(commits)

    if len(issue_ids) > 0:
        update_youtrack_state = prompt_utils.ask_confirm(
            f"Vuoi spostare le card associate in {release_state}?", default=False
        )

        for issue_id in issue_ids:
            try:
                youtrack.comment(
                    issue_id,
                    f"Deploy in produzione di {project} effettuato con la release {new_version}",
                )
                if update_youtrack_state:
                    youtrack.update_state(issue_id, release_state)
                    logger.info(f"{issue_id} spostata in {release_state}")
            except Exception:
                logger.warning(
                    f"Si è verificato un errore durante lo spostamento della card {issue_id} in {release_state}"
                )

    create_release(repo, new_version, message, project)


def get_release(repo):
    with Halo(text="Loading...", spinner="dots", color="magenta"):
        latest_release = github.get_latest_release_if_exists(repo)
        tags = repo.get_tags()
        tag = git.get_last_tag_number(tags)
    if latest_release and latest_release.title == tag:
        logger.info(f"La release attuale è {latest_release.title}")
        return latest_release
    logger.info(f"L'ultimo tag trovato è {tag}")
    if not prompt_utils.ask_confirm("Sicuro di voler continuare?"):
        sys.exit(-1)
    return repo.create_git_release(tag, tag, f"New release from tag {tag}")


def create_release(repo, new_version, message, project):
    new_release = repo.create_git_release(
        new_version, new_version, youtrack.replace_card_names_with_md_links(message)
    )
    if new_release:
        logger.info(f"La release è stata creata! Link: {new_release.html_url}")

        drone_url = drone.get_last_build_url(project)
        if drone_url:
            logger.info(f"Puoi seguire il deploy in produzione su {drone_url}")


def bump_versions(current):
    return {
        "patch": semver.bump_patch(current),
        "minor": semver.bump_minor(current),
        "major": semver.bump_major(current),
    }


def deployed_cards_to_string(cards):
    if cards:
        return "\n".join(cards)
    return ""


def check_migrations_deploy(commits):
    if not commits:
        logger.error("ERRORE: nessun commit trovato")
        sys.exit(-1)
    elif len(commits) == 1:
        files_changed = git.files_changed_between_commits("--raw", f"{commits[0].sha}~")
    else:
        files_changed = git.files_changed_between_commits(
            f"{commits[-1].sha}~", commits[0].sha
        )
    if git.migrations_found(files_changed):
        logger.warning("ATTENZIONE: migrations rilevate nel codice")
        if not prompt_utils.ask_confirm("Sicuro di voler continuare?"):
            sys.exit(-1)


def stop_if_prod_locked(project, lock):
    request = lock.status(project, "production")

    if request.status_code != 200:
        logger.error("Impossibile determinare lo stato del lock su master.")
        sys.exit(-1)

    request_object = request.json()
    if request_object["locked"]:
        logger.error(
            f"Il progetto è lockato in produzione da {request_object['by']}. Impossibile continuare."
        )
        sys.exit(-1)
