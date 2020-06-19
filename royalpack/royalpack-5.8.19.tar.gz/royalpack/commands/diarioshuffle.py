from typing import *
import royalnet.commands as rc
import royalnet.utils as ru
from sqlalchemy import func

from ..tables import Diario


class DiarioshuffleCommand(rc.Command):
    name: str = "diarioshuffle"

    description: str = "Cita una riga casuale del diario."

    aliases = ["dis", "dishuffle", "dish"]

    syntax = ""

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        DiarioT = self.alchemy.get(Diario)
        entry: List[Diario] = await ru.asyncify(
            data.session
                .query(DiarioT)
                .order_by(func.random())
                .limit(1)
                .one_or_none
        )
        if entry is None:
            raise rc.CommandError("Nessuna riga del diario trovata.")
        await data.reply(f"ℹ️ {entry}")
