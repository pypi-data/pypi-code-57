import discord
from typing import *
import royalnet.commands as rc
from royalnet.serf.discord import *


class DiscordSkipEvent(rc.Event):
    name = "discord_skip"

    async def run(self,
                  guild_id: Optional[int] = None,
                  **kwargs) -> dict:
        if not isinstance(self.serf, DiscordSerf):
            raise rc.UnsupportedError()
        client: discord.Client = self.serf.client
        if len(self.serf.voice_players) == 1:
            voice_player: VoicePlayer = self.serf.voice_players[0]
        else:
            if guild_id is None:
                # TODO: trovare un modo per riprodurre canzoni su più server da Telegram
                raise rc.InvalidInputError("Non so in che Server riprodurre questo file...\n"
                                        "Invia il comando su Discord, per favore!")
            guild: discord.Guild = client.get_guild(guild_id)
            if guild is None:
                raise rc.InvalidInputError("Impossibile trovare il Server specificato.")
            candidate_players = self.serf.find_voice_players(guild)
            if len(candidate_players) == 0:
                raise rc.UserError("Il bot non è in nessun canale vocale.\n"
                                   "Evocalo prima con [c]summon[/c]!")
            elif len(candidate_players) == 1:
                voice_player = candidate_players[0]
            else:
                raise rc.CommandError("Non so su che Server saltare canzone...\n"
                                      "Invia il comando su Discord, per favore!")
        # Stop the playback of the current song
        voice_player.voice_client.stop()
        # Done!
        return {}
