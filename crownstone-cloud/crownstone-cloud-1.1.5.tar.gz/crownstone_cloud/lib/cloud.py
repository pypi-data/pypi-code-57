import hashlib
import logging
import asyncio
import aiohttp
from typing import Optional
from crownstone_cloud._RequestHandlerInstance import RequestHandler
from crownstone_cloud.lib.cloudModels.spheres import Spheres
from crownstone_cloud.lib.cloudModels.crownstones import Crownstone

_LOGGER = logging.getLogger(__name__)


class CrownstoneCloud:
    """Create a Crownstone lib hub"""

    def __init__(
            self,
            email: str,
            password: str,
            loop: asyncio.AbstractEventLoop = None,
            websession: aiohttp.ClientSession = None
    ) -> None:
        self.login_data = {'email': email, 'password': self.password_to_hash(password)}
        self.loop = loop or asyncio.get_event_loop()
        # set request handler params
        RequestHandler.websession = websession or aiohttp.ClientSession(loop=loop)
        RequestHandler.login_data = self.login_data
        # data
        self.spheres: Optional[Spheres] = None

    async def initialize(self) -> None:
        """Async initialize the cloud data"""
        if RequestHandler.access_token is None:
            await self.login()
        await self.sync()

    def initialize_sync(self) -> None:
        """Sync initialize the cloud data"""
        self.loop.run_until_complete(self.initialize())

    @staticmethod
    def set_access_token(access_token: str) -> None:
        RequestHandler.access_token = access_token

    @staticmethod
    def get_access_token() -> str:
        return RequestHandler.access_token

    async def login(self) -> None:
        """Login to Crownstone API"""
        result = await RequestHandler.post('users', 'login', json=self.login_data)

        # Set access token & user id
        RequestHandler.access_token = result['id']
        self.spheres = Spheres(self.loop, result['userId'])

        _LOGGER.info("Login to Crownstone Cloud successful")

    async def sync(self) -> None:
        """Sync all data from cloud"""
        _LOGGER.info("Initiating all cloud data, please wait...")
        # get the sphere data
        await self.spheres.update()

        # get the data from the sphere attributes
        for sphere in self.spheres:
            await asyncio.gather(
                sphere.update_sphere_presence(),
                sphere.crownstones.update(),
                sphere.locations.update(),
                sphere.users.update()
            )
        _LOGGER.info("Cloud data successfully initialized")

    def get_crownstone(self, crownstone_name) -> Crownstone:
        """Get a crownstone by name without specifying a sphere"""
        for sphere in self.spheres:
            for crownstone in sphere.crownstones:
                if crownstone.name == crownstone_name:
                    return crownstone

    def get_crownstone_by_id(self, crownstone_id) -> Crownstone:
        """Get a crownstone by id without specifying a sphere"""
        for sphere in self.spheres:
            return sphere.crownstones[crownstone_id]

    @staticmethod
    def reset() -> None:
        """Cleanup the request handler instance data"""
        RequestHandler.access_token = None
        RequestHandler.login_data = None

    @staticmethod
    async def close_session() -> None:
        """Close the websession after we are done"""
        await RequestHandler.websession.close()
        _LOGGER.warning("Session closed.")

    def close_session_sync(self) -> None:
        """Sync version of close session"""
        self.loop.run_until_complete(self.close_session())

    @staticmethod
    def password_to_hash(password):
        """Generate a sha1 password from string"""
        if password is None:
            return None
        pw_hash = hashlib.sha1(password.encode('utf-8'))
        return pw_hash.hexdigest()
