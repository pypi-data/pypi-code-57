from .server import Server
from .validate import Validate
from .routes import ROUTES
from .misc import Misc

import aiohttp
import asyncio
from urllib.parse import urlencode

class client(Misc):
    """ PES API Interface. """

    def __init__(self, api_key, session=None):
        self.ROUTES = ROUTES
        
        self.headers = {"Authorization": api_key}

        if session:
            self.session = session
        else:
            self.session = aiohttp.ClientSession(loop=asyncio.get_event_loop())

        self.validate = Validate(obj=self)

    def server(self, server_id=None):
        """ Server Object
                - server_id, not required.
        """
        return Server(server_id=server_id, obj=self)

    def query_string(self, route, given_vars: dict):
        return route + "?" + urlencode(given_vars)

    def path_var(self, route, given_vars: str):
        return route + "/" + given_vars

    async def _get(self, return_json=True, **kwargs):
        async with self.session.get(headers=self.headers, **kwargs) as resp:
            if resp.status == 200:
                if return_json:
                    return await resp.json()
                else:
                    return await resp.read()
            else:
                return False

    async def _post(self, **kwargs):
        async with self.session.post(headers=self.headers, **kwargs) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                return False

    async def _put(self, **kwargs):
        async with self.session.put(headers=self.headers, **kwargs) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                return False

    async def _delete(self, **kwargs):
        async with self.session.delete(headers=self.headers, **kwargs) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                return False