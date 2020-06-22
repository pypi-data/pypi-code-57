from .server import Server

from .routes import ROUTES

from .resources import CONFIG

from .validate import Validate

from .models.server import ServerModel
from .models.locations import LocationModel
from .models.mapgroups import MapGroupsModel
from .models.gamemodes import GameModesModel
from .models.files import FilesModel

from .wrapped_requests import AWR

import aiohttp


__version__ = "1.0.0"


class client:
    validate = Validate()

    def __init__(self, api_key: str, session: aiohttp.ClientSession = None):
        """ Client for interacting with PES's API.

        api_key: str
            Pes API key.
        session: aiohttp.ClientSession
            Optionally pass your own aiohttp ClientSession.
        """

        CONFIG.api_key = {
            "Authorization": api_key
        }

        if session:
            CONFIG.session = session
        else:
            CONFIG.session = aiohttp.ClientSession()

    async def close(self):
        """ Closes all active sessions """

        await CONFIG.session.close()

    def server(self, server_id=None):
        """ Used for interacting with a server.
                server_id: str
                    If creating a server, server_id
                    will be set to the created server ID.
        """

        return Server(server_id)

    async def servers(self, **kwargs):
        """ https://api.pacifices.cloud/docs.html#servers-servers
                Lists servers matching those parameters.
        """

        data = await AWR(
            ROUTES.server_base,
            params=kwargs
        ).get()

        for server in data["result"]:
            yield ServerModel(server), Server(server["id"])

    async def locations(self):
        """ https://api.pacifices.cloud/docs.html#locations-locations-get
                Get all available locations where you can deploy a server.
        """

        data = await AWR(
            ROUTES.locations
        ).get()

        for location in data["result"]:
            yield LocationModel(location)

    async def mapgroups(self):
        """ https://api.pacifices.cloud/docs.html#mapgroups
                Get all available mapgroups.
        """

        data = await AWR(
            ROUTES.mapgroups
        ).get()

        for map_group in data["result"].values():
            yield MapGroupsModel(map_group)

    async def mods(self):
        """ https://api.pacifices.cloud/docs.html#mods-mods-get
                Get all available mods.
        """

        data = await AWR(
            ROUTES.mods
        ).get()

        return data["result"]

    async def plugins(self):
        """ https://api.pacifices.cloud/docs.html#plugins
                Get all available plugins.
        """

        data = await AWR(
            ROUTES.plugins
        ).get()

        return data["result"]

    async def tickrates(self):
        """ https://api.pacifices.cloud/docs.html#tickrates-tickrates-get
                Get all available tickrates.
        """

        data = await AWR(
            ROUTES.tickrates
        ).get()

        return data["result"]

    async def gamemodes(self):
        """ https://api.pacifices.cloud/docs.html#gamemodes-gamemodes-get
                Get all available gamemodes.
        """

        data = await AWR(
            ROUTES.gamemodes
        ).get()

        for gamemode in data["result"].values():
            yield GameModesModel(gamemode)

    async def files(self):
        """ https://api.pacifices.cloud/docs.html#files
                Get all available files.
        """

        data = await AWR(
            ROUTES.files
        ).get()

        for file in data["result"]:
            yield FilesModel(file)
