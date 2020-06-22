import royalnet.utils as ru
from royalnet.constellation.api import *


class ApiDiscordCvStar(ApiStar):
    path = "/api/discord/cv/v1"

    tags = ["discord"]

    async def get(self, data: ApiData) -> ru.JSON:
        """Get the members status of a single Discord guild.

        Equivalent to calling /cv in a chat."""
        response = await self.interface.call_herald_event("discord", "discord_cv")
        return response
