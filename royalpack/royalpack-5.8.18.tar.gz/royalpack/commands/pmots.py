from typing import *
import royalnet.commands as rc


class PmotsCommand(rc.Command):
    name: str = "pmots"

    description: str = "Confondi Proto!"

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        await data.reply("👣 pmots pmots")
