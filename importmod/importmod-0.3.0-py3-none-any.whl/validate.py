# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import urllib
from logging import debug, error

from portmod.pybuild import MD5
from portmod.repo.loader import load_all
from portmod.repo.usestr import use_reduce

from .sources.nexus import parse_nexus_url, validate_file


def validate_all_files():
    for mod in load_all():
        debug(f"Validating {mod}...")
        if hasattr(mod, "NEXUS_URL"):
            for source in mod.get_sources(matchall=True):
                if not urllib.parse.urlparse(source.url).hostname:
                    debug(f"Validating {source.name} for {mod}...")
                    hash_value = source.hashes.get(MD5)
                    nexus_urls = use_reduce(mod.NEXUS_URL, matchall=True, flat=True)
                    game_mod_ids = [parse_nexus_url(url) for url in nexus_urls]
                    if not any(
                        validate_file(game, mod_id, source.name, hash_value)
                        for game, mod_id in game_mod_ids
                    ):
                        error(
                            f"Hash failed for {mod} with value {hash_value}.\n\t{mod.NEXUS_URL}"
                        )
