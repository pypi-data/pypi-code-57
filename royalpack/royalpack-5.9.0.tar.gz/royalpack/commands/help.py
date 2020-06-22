from typing import *
import royalnet
import royalnet.commands as rc


class HelpCommand(rc.Command):
    name: str = "help"

    description: str = "Visualizza informazioni su un comando."

    syntax: str = "{comando}"

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        name: str = args[0].lstrip(self.interface.prefix)

        try:
            command: rc.Command = self.serf.commands[f"{self.interface.prefix}{name}"]
        except KeyError:
            raise rc.InvalidInputError("Il comando richiesto non esiste.")

        message = [
            f"[c]{self.interface.prefix}{command.name} {command.syntax}[/c]",
            "",
            f"{command.description}"
        ]

        await data.reply("\n".join(message))
