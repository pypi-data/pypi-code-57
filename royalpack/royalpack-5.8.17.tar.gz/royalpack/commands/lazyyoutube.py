from typing import *
from .lazyplay import LazyplayCommand


class LazyyoutubeCommand(LazyplayCommand):
    name: str = "lazyyoutube"

    aliases = ["lyt"]

    description: str = "Cerca un video su YouTube e lo aggiunge (lazy) alla coda della chat vocale."

    syntax = "{ricerca}"

    async def get_urls(self, args):
        return [f"ytsearch:{args.joined()}"]
