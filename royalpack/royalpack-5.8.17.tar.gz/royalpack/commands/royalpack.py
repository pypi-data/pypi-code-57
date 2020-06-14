from typing import *
import royalnet.commands as rc

from ..version import semantic


class RoyalpackCommand(rc.Command):
    name: str = "royalpack"

    description: str = "Visualizza la versione attuale di Royalpack."

    syntax: str = ""

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        if __debug__:
            message = f"ℹ️ Royalpack [url=https://github.com/Steffo99/royalpack/]Unreleased[/url]\n"
        else:
            message = f"ℹ️ Royalpack [url=https://github.com/Steffo99/royalpack/releases/tag/{semantic}]{semantic}[/url]\n"
        if "69" in semantic:
            message += "(Nice.)"
        await data.reply(message)
