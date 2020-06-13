import aiohttp
from aiohttp import *

class taromaruInit():

    def __init__(self):
        self.apikey = None

    def setapikey(self, apikey):
        self.apikey = apikey

    async def image(self, type):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://doggo-clicker.000webhostapp.com/api/{type}/', params={
                "apikey": self.apikey,
            }) as responce:
                data = await responce.json()
            return data