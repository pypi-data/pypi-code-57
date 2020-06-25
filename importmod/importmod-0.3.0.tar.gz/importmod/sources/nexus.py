# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""Utility functions for interacting with nexusmods.com"""

import json
import os
import urllib
from collections import namedtuple
from logging import warning
from typing import Tuple

import requests
from portmod.repo import Atom
from portmod.repo.util import get_max_version

from ..atom import parse_name, parse_version
from ..config import NEXUS_KEY

NexusData = namedtuple(
    "NexusData",
    ["atom", "modid", "name", "desc", "files", "homepage", "author", "nudity"],
)


class APILimitExceeded(Exception):
    """Exception indicating that the NexusApi's daily limit has been exceeded"""


def parse_nexus_url(url: str) -> Tuple[str, int]:
    parsed = urllib.parse.urlparse(url)
    game = parsed.path.split("/")[1]
    mod_id = int(parsed.path.split("/")[3])
    return game, mod_id


def get_nexus_info(game: str, modid: int) -> NexusData:
    """
    Fetches mod information from nexusmods.com and parses it into a NexusData object
    """
    info_url = f"https://api.nexusmods.com/v1/games/{game}/mods/{modid}/"
    files_url = f"https://api.nexusmods.com/v1/games/{game}/mods/{modid}/files/"

    headers = {"APIKEY": NEXUS_KEY, "content-type": "application/json"}

    rinfo = requests.get(info_url, headers=headers)
    if rinfo.headers["X-RL-Daily-Remaining"] == 0:
        raise APILimitExceeded()

    rfiles = requests.get(files_url, headers=headers)

    if rinfo.status_code == rfiles.status_code == requests.codes.ok:
        info = json.loads(rinfo.text)
        files = json.loads(rfiles.text)
    else:
        rinfo.raise_for_status()
        rfiles.raise_for_status()

    version = parse_version(info["version"]) or "0.1"

    # Select all files except those in the OLD_VERSION category
    tmpfiles = [
        file
        for file in files["files"]
        if file["category_name"] != "OLD_VERSION" and file["category_name"]
    ]

    allversions = [version]
    for file in tmpfiles:
        tmp_ver = parse_version(file["version"])
        if tmp_ver:
            allversions.append(tmp_ver)

    # Mod author may not have updated the mod version.
    # Version used should be the newest file version among the files we selected
    version = get_max_version(allversions)

    atom = Atom(parse_name(info["name"]) + "-" + version)

    files = []
    minorversion = None
    for file in tmpfiles:
        skip = False

        # Ignore exe files. We can't use them anyway
        _, ext = os.path.splitext(file["file_name"])
        if ext == ".exe":
            skip = True

        for otherfile in tmpfiles:
            # Base name is the same, but filename is different.
            # That is, they've uploaded a new version but didn't change the version
            # Let's change it for them to avoid conflicts
            if (
                file["name"] == otherfile["name"]
                and file["file_name"] != otherfile["file_name"]
            ):
                if minorversion is None:
                    minorversion = 1
                else:
                    minorversion += 1

                if file["file_name"] < otherfile["file_name"]:
                    skip = True
                    break

        if not skip:
            files.append(file)

    return NexusData(
        atom=Atom(atom + (str(minorversion or ""))),
        modid=modid,
        name=info["name"],
        desc=info["summary"].replace("\\", ""),
        files=[file["file_name"].replace(" ", "_") for file in files],
        homepage=f"https://www.nexusmods.com/{game}/mods/{modid}",
        author=info["author"],
        nudity=info["contains_adult_content"],
    )


def validate_file(game, mod_id, file, hash):
    hash_url = f"https://api.nexusmods.com/v1/games/{game}/mods/md5_search/{hash}.json"

    headers = {"APIKEY": NEXUS_KEY, "content-type": "application/json"}

    response = requests.get(hash_url, headers=headers)

    if response.status_code == requests.codes.not_found:
        return False

    mods = json.loads(response.text)
    for mod in mods:
        if mod["mod"]["mod_id"] == mod_id:
            return True

    modnames = [mod.get("mod").get("name") for mod in mods]
    if all(mod.get("mod").get("status") == "hidden" for mod in mods):
        warning("Hidden mods matched the file!")
        return True
    Exception(f"Invalid response {modnames} from NexusMods API when hashing {file}")


def get_nexus_updates(game: str, period: str, mod_map):
    """
    Returns a list of updates to nexusmods.com mods in the given period

    Valid periods are 1d, 1w, 1m
    """
    assert period in ["1d", "1w", "1m"]
    update_url = (
        f"https://api.nexusmods.com/v1/games/{game}/mods/updated.json?period={period}"
    )

    headers = {"APIKEY": NEXUS_KEY, "content-type": "application/json"}

    uinfo = requests.get(update_url, headers=headers)
    if uinfo.headers["X-RL-Daily-Remaining"] == 0:
        raise APILimitExceeded()

    if uinfo.status_code == requests.codes.ok:
        info = json.loads(uinfo.text)
    else:
        uinfo.raise_for_status()

    updates = []

    for mod in info:
        if (game, mod["mod_id"]) in mod_map:
            localmod = mod_map[(game, mod["mod_id"])]
            nexus_info = get_nexus_info(game, mod["mod_id"])
            newest = nexus_info.atom.MV
            if (
                newest != localmod.MV
                and get_max_version([newest, localmod.MV]) == newest
            ):
                updates.append(nexus_info)
    return updates
