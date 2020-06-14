from typing import *
import royalnet.commands as rc
import royalnet.backpack.tables as rbt

from ..tables import FiorygiTransaction


class MagickfiorygiCommand(rc.Command):
    name: str = "magickfiorygi"

    description: str = "Crea fiorygi dal nulla."

    syntax: str = "{destinatario} {quantità} {motivo}"

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        author = await data.get_author(error_if_none=True)
        if "banker" not in author.roles:
            raise rc.UserError("Non hai permessi sufficienti per eseguire questo comando.")

        user_arg = args[0]
        qty_arg = args[1]
        reason_arg = " ".join(args[2:])

        if user_arg is None:
            raise rc.InvalidInputError("Non hai specificato un destinatario!")
        user = await rbt.User.find(self.alchemy, data.session, user_arg)
        if user is None:
            raise rc.InvalidInputError("L'utente specificato non esiste!")

        if qty_arg is None:
            raise rc.InvalidInputError("Non hai specificato una quantità!")
        try:
            qty = int(qty_arg)
        except ValueError:
            raise rc.InvalidInputError("La quantità specificata non è un numero!")

        if reason_arg == "":
            raise rc.InvalidInputError("Non hai specificato un motivo!")

        await FiorygiTransaction.spawn_fiorygi(data, user, qty, reason_arg)
