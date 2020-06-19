from typing import *
import royalnet.commands as rc
import aiohttp
import io


class CatCommand(rc.Command):
    name: str = "cat"

    description: str = "Invia un gatto casuale in chat."

    syntax: str = ""

    aliases = ["catto", "kat", "kitty", "kitten", "gatto", "miao", "garf", "basta"]

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.thecatapi.com/v1/images/search") as response:
                if response.status >= 400:
                    raise rc.ExternalError(f"Request returned {response.status}")
                result = await response.json()
                assert len(result) == 1
                cat = result[0]
                assert "url" in cat
                url = cat["url"]
            async with session.get(url) as response:
                img = await response.content.read()
                await data.reply_image(image=io.BytesIO(img))
