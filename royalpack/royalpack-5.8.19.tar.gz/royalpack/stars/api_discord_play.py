from typing import *
from royalnet.constellation.api import *
import logging


log = logging.getLogger(__name__)


class ApiDiscordPlayStar(ApiStar):
    path = "/api/discord/play/v1"

    summary = "Add a audio file to the RoyalQueue of a Discord Guild."

    parameters = {
        "url": "The url of the audio file to add.",
        "user": "The name to display in the File Added message.",
        "guild_id": "The id of the guild owning the RoyalQueue to add the audio file to."
    }

    tags = ["discord"]

    async def api(self, data: ApiData) -> dict:
        url = data["url"]
        user = data.get("user")
        guild_id_str = data.get("guild_id")
        if guild_id_str:
            try:
                guild_id: Optional[int] = int(guild_id_str)
            except (ValueError, TypeError):
                raise InvalidParameterError("'guild_id' is not a valid int.")
        else:
            guild_id = None
        log.info(f"Received request to play {url} on guild_id {guild_id} via web")
        response = await self.interface.call_herald_event("discord", "discord_play",
                                                          urls=[url],
                                                          guild_id=guild_id,
                                                          user=user)
        return response
