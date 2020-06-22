from typing import *
import royalnet.commands as rc
import royalnet.backpack.tables as rbt


class ExecCommand(rc.Command):
    # oh god if there is a security vulnerability
    name: str = "exec"

    description: str = "Esegui uno script Python... se sei Steffo."

    syntax: str = "{script}"

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        user: rbt.User = await data.get_author(error_if_none=True)
        if "admin" not in user.roles:
            raise rc.CommandError("Non sei autorizzato a eseguire codice arbitrario!\n"
                               "(Sarebbe un po' pericoloso se te lo lasciassi eseguire, non trovi?)")
        try:
            exec(args.joined(require_at_least=1))
        except Exception as e:
            raise rc.CommandError(f"Esecuzione fallita: {e}")
        await data.reply(f"✅ Fatto!")
