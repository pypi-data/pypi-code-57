from typing import *
from .lazyplay import LazyplayCommand


class LazyyahoovideoCommand(LazyplayCommand):
    name: str = "lazyyahoovideo"

    aliases = ["lyv"]

    description: str = "Cerca un video su Yahoo Video e lo aggiunge (lazy) alla coda della chat vocale."

    syntax = "{ricerca}"

    async def get_urls(self, args):
        return [f"yvsearch:{args.joined()}"]

    # Too bad yvsearch: always finds nothing.
