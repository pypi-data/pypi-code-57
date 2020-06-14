from typing import *
import discord
import asyncio as aio
import royalnet.commands as rc
import royalnet.backpack.tables as rbt


class PlayCommand(rc.Command):
    name: str = "play"

    aliases = ["p"]

    description: str = "Aggiunge un url alla coda della chat vocale."

    syntax = "{url}"

    async def get_urls(self, args: rc.CommandArgs):
        url = args.joined(require_at_least=1)
        if not (url.startswith("http://") or url.startswith("https://")):
            raise rc.InvalidInputError(f"L'URL specificato non inizia con il nome di un protocollo supportato"
                                       f" ([c]http://[/c] o [c]https://[/c]).")
        return [url]

    def get_embed_color(self) -> Optional[int]:
        return None

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

        urls = await self.get_urls(args)

        play_task: aio.Task = self.loop.create_task(
            self.interface.call_herald_event("discord", "discord_play",
                                             urls=urls,
                                             guild_id=guild_id,
                                             user=user_str,
                                             force_color=self.get_embed_color())
        )

        if len(urls) > 1:
            await data.reply("⌛ Attendi qualche minuto...")
        else:
            await data.reply("⌛ Attendi un attimo...")

        await play_task
