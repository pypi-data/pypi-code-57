from typing import *
import royalnet
import royalnet.commands as rc
import royalnet.utils as ru
from ..tables import Treasure


class MagicktreasureCommand(rc.Command):
    name: str = "magicktreasure"

    description: str = "Crea un nuovo Treasure di Fiorygi (senza spendere i tuoi)."

    syntax: str = "{codice} {valore}"

    async def _permission_check(self, author, code, value, data):
        if "banker" not in author.roles:
            raise rc.UserError("Non hai permessi sufficienti per eseguire questo comando.")
        return author

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

        return treasure

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        await data.delete_invoking()
        author = await data.get_author(error_if_none=True)

        code = args[0].lower()
        try:
            value = int(args[1])
        except ValueError:
            raise rc.InvalidInputError("Il valore deve essere maggiore o uguale a 0.")
        if value < 0:
            raise rc.InvalidInputError("Il valore deve essere maggiore o uguale a 0.")

        await self._permission_check(author, code, value, data)
        treasure = await self._create_treasure(author, code, value, data)

        data.session.add(treasure)
        await data.session_commit()

        await data.reply("✅ Treasure creato!")
