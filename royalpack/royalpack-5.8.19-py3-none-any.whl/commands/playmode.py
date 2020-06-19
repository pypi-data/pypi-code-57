from typing import *
import royalnet.commands as rc
import discord
import royalnet.backpack.tables as rbt


class PlaymodeCommand(rc.Command):
    name: str = "playmode"

    aliases = ["pm"]

    description: str = "Seleziona la modalità di riproduzione musicale."

    syntax: str = "{queue|pool}"

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        if self.interface.name == "discord":
            message: discord.Message = data.message
            guild: discord.Guild = message.guild
            if guild is None:
                guild_id = None
            else:
                guild_id: Optional[int] = guild.id
        else:
            guild_id = None

        user: rbt.User = await data.get_author()
        user_str = None

        if user is not None:
            try:
                user_discord: rbt.Discord = user.discord[0]
            except (AttributeError, IndexError):
                user_str = str(user)
            else:
                user_str = str(f"<@{user_discord.discord_id}>")

        response = await self.interface.call_herald_event("discord", "discord_playmode",
                                                          playable_string=args[0],
                                                          guild_id=guild_id,
                                                          user=user_str)

        if response["name"] == "RoyalQueue":
            await data.reply(f"✅ Modalità di riproduzione impostata a [b]Queue[/b]:\n"
                             f"- Riproduci le canzoni nell'ordine scelto\n"
                             f"- Rimuovi le canzoni dopo averle riprodotte")

        elif response["name"] == "RoyalPool":
            await data.reply(f"✅ Modalità di riproduzione impostata a [b]Pool[/b]:\n"
                             f"- Aggiungi canzoni al pool con [c]!p[/c], [c]!yt[/c] e [c]!fw[/c]\n"
                             f"- Riproduci all'infinito canzoni casuali dal pool\n"
                             f"- Non è possibile rimuovere canzoni dal pool, [c]!skip[/c]parle manderà solo avanti il pool\n"
                             f"- Interrompi la riproduzione del pool cambiando modalità di riproduzione")

        else:
            await data.reply(f"✅ Modalità di riproduzione impostata a [c]{response['name']}[/c]!")