from typing import *
from .lazyplay import LazyplayCommand


class LazysoundcloudCommand(LazyplayCommand):
    name: str = "lazysoundcloud"

    aliases = ["lsc"]

    description: str = "Cerca un video su SoundCloud e lo aggiunge (lazy) alla coda della chat vocale."

    syntax = "{ricerca}"

    async def get_urls(self, args):
        return [f"scsearch:{args.joined()}"]
