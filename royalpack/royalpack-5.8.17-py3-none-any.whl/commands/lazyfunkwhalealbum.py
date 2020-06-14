from typing import *
import royalnet.commands as rc
import aiohttp
import urllib.parse

from .lazyplay import LazyplayCommand


class LazyfunkwhalealbumCommand(LazyplayCommand):
    name: str = "lazyfunkwhalealbum"

    aliases = ["lfwa", "lfwalbum", "lazyfunkwhalea"]

    description: str = "Cerca un album su RoyalWhale e aggiungilo (lazy) alla coda della chat vocale."

    syntax = "{ricerca}"

    def get_embed_color(self):
        return 0x009FE3

    async def get_urls(self, args):
        search = urllib.parse.quote(args.joined(require_at_least=1))
        async with aiohttp.ClientSession() as session:
            async with session.get(self.config["Funkwhale"]["instance_url"] +
                                   f"/api/v1/search?query={search}") as response:
                if response.status >= 400:
                    raise rc.ExternalError(f"Request returned {response.status}")
                j = await response.json()
        if len(j["albums"]) < 1:
            raise rc.UserError("Nessun file audio trovato con il nome richiesto.")
        album = j["albums"][0]
        return [f'{self.config["Funkwhale"]["instance_url"]}{track["listen_url"]}' for track in album["tracks"]]
