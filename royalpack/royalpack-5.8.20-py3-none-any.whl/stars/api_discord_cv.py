from royalnet.constellation.api import *


class ApiDiscordCvStar(ApiStar):
    path = "/api/discord/cv/v1"

    summary = "Get the members status of a single Discord guild. Equivalent to calling /cv in a chat."

    tags = ["discord"]

    async def api(self, data: ApiData) -> dict:
        response = await self.interface.call_herald_event("discord", "discord_cv")
        return response
