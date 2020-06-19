from typing import *
import royalnet
import royalnet.commands as rc
import royalnet.utils as ru
from ..tables import Treasure, FiorygiTransaction
from .magicktreasure import MagicktreasureCommand


class GivetreasureCommand(MagicktreasureCommand):
    name: str = "givetreasure"

    description: str = "Crea un nuovo Treasure di Fiorygi (usando il tuo credito)"

    syntax: str = "{codice} {valore}"

    async def _permission_check(self, author, code, value, data):
        if author.fiorygi.fiorygi < value:
            raise rc.UserError("Non hai abbastanza fiorygi per creare questo Treasure.")

    async def _create_treasure(self, author, code, value, data):
        TreasureT = self.alchemy.get(Treasure)

        treasure = await ru.asyncify(data.session.query(TreasureT).get, code)
        if treasure is not None:
            raise rc.UserError("Esiste già un Treasure con quel codice.")

        treasure = TreasureT(
            code=code,
            value=value,
            redeemed_by=None
        )

        await FiorygiTransaction.spawn_fiorygi(data, author, -value, "aver creato un tesoro")

        return treasure
