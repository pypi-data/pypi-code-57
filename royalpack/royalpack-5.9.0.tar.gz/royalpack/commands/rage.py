from typing import *
import random
import royalnet.commands as rc


class RageCommand(rc.Command):
    name: str = "rage"

    aliases = ["balurage", "madden"]

    description: str = "Arrabbiati per qualcosa, come una software house californiana."

    _MAD = [
        "MADDEN MADDEN MADDEN MADDEN",
        "EA bad, praise Geraldo!",
        "Stai sfogando la tua ira sul bot!",
        "Basta, io cambio gilda!",
        "Fondiamo la RRYG!"
    ]

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        await data.reply(f"😠 {random.sample(self._MAD, 1)[0]}")
