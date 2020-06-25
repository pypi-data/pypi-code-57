# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import re
from collections import namedtuple
from enum import Enum
from typing import List
from urllib.parse import urlparse

from portmod import Pybuild
from portmod.repo.atom import Atom
from portmod.repo.loader import load_all
from portmod.repo.usestr import use_reduce
from portmod.repo.util import get_max_version

from .atom import parse_atom, parse_version
from .sources.modhistory import get_modhistory_info
from .sources.nexus import get_nexus_info, get_nexus_updates

ModId = namedtuple("ModId", ["source", "id"])


class Update:
    def __init__(self, *, oldatom, location, newatom=None):
        self.oldatom = oldatom
        self.newatom = newatom
        self.location = location
        self.available = newatom is not None

        if self.available:
            self.title = f"[{oldatom.CMN}] Version {newatom.MV} is available"
            self.description = (
                f"Old Version: {oldatom}\\\n"
                f"New Version: {oldatom.CMN}-{newatom.MVR}\n\n"
                f"New version can be found here: {location}\n\n"
                "*Note: this is an automatically generated message. "
                "Please report any issues [here]"
                "(https://gitlab.com/portmod/importmod/issues)*"
            )
        else:
            self.title = (
                f"[{oldatom.CMN}] Mod is no longer available from current source"
            )
            self.description = (
                f"Attempt to check mod availability from: {location} failed.\n\n"
                "*Note: this is an automatically generated message. "
                "Please report any issues [here]"
                "(https://gitlab.com/portmod/importmod/issues)*"
            )


class ModSource(Enum):
    Nexus = 1
    Modhistory = 2


def get_mod_ids(mod):
    ids = []
    nexus_urls = []
    modhistory_urls = []
    if hasattr(mod, "NEXUS_URL"):
        nexus_urls = use_reduce(mod.NEXUS_URL, matchall=True, flat=True)
    else:
        # Check if HOMEPAGE contains a Nexus url
        for url in use_reduce(mod.HOMEPAGE, matchall=True, flat=True):
            hostname = urlparse(url).hostname
            if re.match(r"^\w*\.?nexusmods.com$", hostname):
                nexus_urls.append(url)
            elif re.match("^mw.modhistory.com$", hostname):
                modhistory_urls.append(url)

    for url in nexus_urls:
        game, modid = urlparse(url).path.split("/mods/")
        ids.append(ModId(ModSource.Nexus, (game.lstrip("/"), int(modid))))

    for url in modhistory_urls:
        modid = urlparse(url).path.split("-")[-1]
        ids.append(ModId(ModSource.Modhistory, int(modid)))

    return ids


def get_nexus_id_map():
    """
    Returns a dictionary mapping NexusMod game,id to mod for all NexusMods in database
    """
    id_map = {}
    for mod in load_all():
        ids = get_mod_ids(mod)
        for modid in ids:
            if modid.source == ModSource.Nexus:
                id_map[modid.id] = mod
    return id_map


def get_updates(period: str = None):
    """
    Returns a list of updates since the given time

    @period must be one of 1d, 1w, 1m
    """
    results: List[Update] = []
    if period is None:
        for mod in load_all():
            print(f"Checking {mod} for updates...")
            results += check_for_update(mod)
    else:
        id_map = get_nexus_id_map()
        updates = get_nexus_updates("morrowind", period, id_map)
        for update in updates:
            results.append(
                Update(
                    oldatom=id_map[("morrowind", update.modid)].ATOM,
                    newatom=update.atom,
                    location=update.homepage,
                )
            )
    return results


def check_for_update(mod: Pybuild) -> List[Update]:
    updates = []

    for modid in get_mod_ids(mod):
        if modid.source == ModSource.Nexus:
            game, modid = modid.id
            url = f"https://www.nexusmods.com/{game}/mods/{modid}"
            try:
                nexus_info = get_nexus_info(game, modid)
                newest = parse_version(nexus_info.atom.MV)
                if newest != mod.MV and get_max_version([newest, mod.MV]) == newest:
                    updates.append(
                        Update(
                            oldatom=mod.ATOM,
                            newatom=parse_atom(nexus_info.atom),
                            location=url,
                        )
                    )
                    print(f"Found update for {mod}. New version: {newest}")
            except Exception as e:
                print(f"Unable to check {url}")
                print(e)
                updates.append(Update(oldatom=mod.ATOM, location=url))
        elif modid.source == ModSource.Modhistory:
            # Note that mods on modhistory are not being actively updated, but checking
            # this infrequently may be useful to ensure that the mod is still available
            url = f"http://mw.modhistory.com/download--{modid.id}"
            try:
                info = get_modhistory_info(url)
                newest = info["Version"]
                if newest != mod.MV and get_max_version([newest, mod.MV]) == newest:
                    updates.append(
                        Update(
                            oldatom=mod.ATOM,
                            newatom=Atom(f"{mod.CMN}-{newest}"),
                            location=url,
                        )
                    )
                    print(f"Found update for {mod}. New version: {newest}")

            except Exception as e:
                print(f"Unable to check {url}")
                print(e)
                updates.append(Update(oldatom=mod.ATOM, location=url))

    return updates
