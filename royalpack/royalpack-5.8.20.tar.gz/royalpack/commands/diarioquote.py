from typing import *
import royalnet.commands as rc
import royalnet.utils as ru

from ..tables import Diario


class DiarioquoteCommand(rc.Command):
    name: str = "diarioquote"

    description: str = "Cita una riga del diario."

    aliases = ["dq", "quote", "dquote"]

    syntax = "{id}"

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        try:
            entry_id = int(args[0].lstrip("#"))
        except ValueError:
            raise rc.CommandError("L'id che hai specificato non è valido.")
        entry: Diario = await ru.asyncify(data.session.query(self.alchemy.get(Diario)).get, entry_id)
        if entry is None:
            raise rc.CommandError("Nessuna riga con quell'id trovata.")
        await data.reply(f"ℹ️ {entry}")
