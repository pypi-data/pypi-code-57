# -*- encoding: utf-8 -*-
from distutils.version import StrictVersion
from os import environ
import time
import subprocess
from subprocess import CalledProcessError
import sys
import requests

from halo import Halo
from suite_py.lib.tokens import Tokens
from suite_py.lib.logger import Logger

logger = Logger()
drone_token = environ["DRONE_TOKEN"] = Tokens().drone
baseurl = environ["DRONE_SERVER"] = "https://drone-1.prima.it"


def get_last_build_url(repo, prefix=None):
    with Halo(text="Contacting drone...", spinner="dots", color="magenta"):
        # necessario per far comparire la build che abbiamo appena pushato
        time.sleep(2)
        try:
            builds = requests.get(
                f"{baseurl}/api/repos/primait/{repo}/builds",
                headers={"Authorization": f"Bearer {drone_token}"},
            ).json()

            if prefix:
                builds = [b for b in builds if b["target"].startswith(prefix)]

            return f"{baseurl}/primait/{repo}/{builds[0]['number']}"
        except Exception:
            return ""


def get_pr_build_number(repo, commit_sha):
    with Halo(text="Contacting drone...", spinner="dots", color="magenta"):
        tries = 10
        while tries > 0:
            tries -= 1
            try:
                builds = requests.get(
                    f"{baseurl}/api/repos/primait/{repo}/builds?per_page=100",
                    headers={"Authorization": f"Bearer {drone_token}"},
                ).json()
                builds = [b for b in builds if b["after"] == commit_sha]
                return builds[0]["number"]
            except Exception:
                time.sleep(1)

        return None


def get_user():
    try:
        user = requests.get(
            f"{baseurl}/api/user", headers={"Authorization": f"Bearer {drone_token}"},
        ).json()
        return user
    except Exception:
        return None


def get_build_url(repo, build_number):
    if build_number:
        return f"{baseurl}/primait/{repo}/{build_number}"
    return None


def get_tag_from_builds(repo):
    tags = []
    builds = requests.get(
        f"{baseurl}/api/repos/primait/{repo}/builds?per_page=100",
        headers={"Authorization": f"Bearer {drone_token}"},
    ).json()

    for build in builds:
        if build["event"] == "tag":
            tags.append(build["ref"].replace("refs/tags/", ""))

    tags = list(dict.fromkeys(tags))
    tags.sort(key=StrictVersion, reverse=True)
    return tags


def get_build_from_tag(repo, tag):
    builds = requests.get(
        f"{baseurl}/api/repos/primait/{repo}/builds?per_page=100",
        headers={"Authorization": f"Bearer {drone_token}"},
    ).json()

    for build in builds:
        if build["event"] == "tag":
            if build["ref"].replace("refs/tags/", "") == tag:
                return build["number"]
    return None


def launch_build(repo, build):
    return requests.post(
        f"{baseurl}/api/repos/primait/{repo}/builds/{build}",
        headers={"Authorization": f"Bearer {drone_token}"},
    ).json()


def prestart_success(repo, build_number):
    with Halo(text="Contacting drone...", spinner="dots", color="magenta"):
        tries = 10
        while build_number and tries > 0:
            tries -= 1
            build_status = requests.get(
                f"{baseurl}/api/repos/primait/{repo}/builds/{build_number}",
                headers={"Authorization": f"Bearer {drone_token}"},
            ).json()

            steps = build_status["stages"][0]["steps"]

            for step in steps:
                if step["name"] == "pre-start":
                    if step["status"] == "success":
                        return True
                    break
            time.sleep(3)
        return False


def fmt(project, path):
    try:
        subprocess.run(["drone", "fmt", "--save", ".drone.yml"], cwd=path, check=True)
    except (CalledProcessError) as e:
        logger.error(f"{project}: non sono riuscito a formattare il .drone.yml {e}")
        sys.exit(-1)


def validate(project, path):
    try:
        subprocess.run(
            ["drone", "lint", "--trusted", ".drone.yml"], cwd=path, check=True
        )
    except (CalledProcessError) as e:
        logger.error(f"{project}: il .drone.yml non è valido {e}")
        sys.exit(-1)


def sign(project, path):
    try:
        subprocess.run(
            ["drone", "sign", f"primait/{project}", "--save"], cwd=path, check=True,
        )
    except (CalledProcessError) as e:
        logger.error(f"{project}: non sono riuscito a firmare il .drone.yml {e}")
        sys.exit(-1)
