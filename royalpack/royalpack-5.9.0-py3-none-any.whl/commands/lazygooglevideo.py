from typing import *
from .lazyplay import LazyplayCommand


class LazygooglevideoCommand(LazyplayCommand):
    name: str = "lazygooglevideo"

    aliases = ["lgv"]

    description: str = "Cerca un video su Google Video e lo aggiunge (lazy) alla coda della chat vocale."

    syntax = "{ricerca}"

    async def get_urls(self, args):
        return [f"gvsearch:{args.joined()}"]

    # Too bad gvsearch: always finds nothing.
