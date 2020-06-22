import discord
from typing import *
import royalnet.commands as rc
from royalnet.serf.discord import *


class DiscordPauseEvent(rc.Event):
    name = "discord_pause"

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

        if voice_player.voice_client.is_paused():
            voice_player.voice_client.resume()
            return {"action": "resumed"}
        else:
            voice_player.voice_client.pause()
            return {"action": "paused"}
