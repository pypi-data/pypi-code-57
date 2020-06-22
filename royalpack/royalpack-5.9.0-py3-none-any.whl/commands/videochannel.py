from typing import *
import discord
import royalnet.commands as rc


class VideochannelCommand(rc.Command):
    name: str = "videochannel"

    aliases = ["golive", "live", "video"]

    description: str = "Converti il canale vocale in un canale video."

    syntax = "[nomecanale]"

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        if self.interface.name != "discord":
            raise rc.UnsupportedError(f"{self} non è supportato su {self.interface.name}.")
        bot: discord.Client = self.serf.client
        message: discord.Message = data.message
        channel_name: str = args.optional(0)
        if channel_name:
            guild: Optional[discord.Guild] = message.guild
            if guild is not None:
                channels: List[discord.abc.GuildChannel] = guild.channels
            else:
                channels = bot.get_all_channels()
            matching_channels: List[discord.VoiceChannel] = []
            for channel in channels:
                if isinstance(channel, discord.VoiceChannel):
                    if channel.name == channel_name:
                        matching_channels.append(channel)
            if len(matching_channels) == 0:
                raise rc.InvalidInputError("Non esiste alcun canale vocale con il nome specificato.")
            elif len(matching_channels) > 1:
                raise rc.UserError("Esiste più di un canale vocale con il nome specificato.")
            channel = matching_channels[0]
        else:
            author: discord.Member = message.author
            voice: Optional[discord.VoiceState] = author.voice
            if voice is None:
                raise rc.InvalidInputError("Non sei connesso a nessun canale vocale.")
            channel = voice.channel
            if author.is_on_mobile():
                await data.reply(f"📹 Per entrare in modalità video, clicca qui:\n"
                                 f"<https://discordapp.com/channels/{channel.guild.id}/{channel.id}>\n"
                                 f"[b]Attenzione: la modalità video non funziona su Android e iOS![/b]")
                return
        await data.reply(f"📹 Per entrare in modalità video, clicca qui:\n"
                         f"<https://discordapp.com/channels/{channel.guild.id}/{channel.id}>")
