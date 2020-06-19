from typing import *
import royalnet.commands as rc
import aiohttp
import io


class PugCommand(rc.Command):
    name: str = "pug"

    description: str = "Invia un carlino casuale in chat."

    syntax: str = ""

    aliases = ["carlino", "carlo", "mallllco"]

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://dog.ceo/api/breed/pug/images/random") as response:
                if response.status >= 400:
                    raise rc.ExternalError(f"Request returned {response.status}")
                result = await response.json()
                assert "status" in result
                assert result["status"] == "success"
                assert "message" in result
                url = result["message"]
            async with session.get(url) as response:
                img = await response.content.read()
                await data.reply_image(image=io.BytesIO(img))
