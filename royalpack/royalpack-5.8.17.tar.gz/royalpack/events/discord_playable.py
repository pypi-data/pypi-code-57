import datetime
from typing import *

import discord
import royalnet.commands as rc
import royalnet.serf.discord as rsd
import royalnet.bard.discord as rbd

from ..utils import RoyalQueue, RoyalPool


class DiscordPlaymodeEvent(rc.Event):
    name = "discord_playmode"

    async def run(self,
                  playable_string: str,
                  guild_id: Optional[int] = None,
                  user: Optional[str] = None,
                  **kwargs) -> dict:
        if not isinstance(self.serf, rsd.DiscordSerf):
            raise rc.UnsupportedError()

        serf: rsd.DiscordSerf = self.serf
        client: discord.Client = self.serf.client
        guild: discord.Guild = client.get_guild(guild_id) if guild_id is not None else None
        candidate_players: List[rsd.VoicePlayer] = serf.find_voice_players(guild)

        if len(candidate_players) == 0:
            raise rc.UserError("Il bot non è in nessun canale vocale.\n"
                               "Evocalo prima con [c]summon[/c]!")
        elif len(candidate_players) == 1:
            voice_player = candidate_players[0]
        else:
            raise rc.CommandError("Non so a che Server cambiare Playable...\n"
                                  "Invia il comando su Discord, per favore!")

        if playable_string.upper() == "QUEUE":
            playable = await RoyalQueue.create()
        elif playable_string.upper() == "POOL":
            playable = await RoyalPool.create()
        else:
            raise rc.InvalidInputError(f"Unknown playable '{playable_string.upper()}'")

        await voice_player.change_playing(playable)

        return {
            "name": f"{playable.__class__.__qualname__}"
        }
