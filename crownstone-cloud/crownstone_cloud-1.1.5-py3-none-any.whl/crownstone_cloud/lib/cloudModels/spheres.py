from crownstone_cloud._RequestHandlerInstance import RequestHandler
from crownstone_cloud.lib.cloudModels.crownstones import Crownstones
from crownstone_cloud.lib.cloudModels.locations import Locations
from crownstone_cloud.lib.cloudModels.users import Users
from typing import Optional
import asyncio


class Spheres:
    """Handler for the spheres of the user"""

    def __init__(self, loop: asyncio.AbstractEventLoop, user_id: str) -> None:
        """Init"""
        self.loop = loop
        self.spheres: Optional[dict] = None
        self.user_id = user_id

    def __iter__(self):
        """Iterate over spheres"""
        return iter(self.spheres.values())

    async def update(self) -> None:
        """
        Get the spheres for the user from the cloud
        This will replace all current data with new data from the cloud
        """
        # get sphere data
        self.spheres = {}
        sphere_data = await RequestHandler.get('users', 'spheres', model_id=self.user_id)
        for sphere in sphere_data:
            self.spheres[sphere['id']] = Sphere(self.loop, sphere, self.user_id)

    def update_sync(self) -> None:
        """Sync function for updating the cloud data"""
        self.loop.run_until_complete(self.update())

    def find(self, sphere_name: str) -> object or None:
        """Search for a sphere by name and return sphere object if found"""
        for sphere in self.spheres.values():
            if sphere_name == sphere.name:
                return sphere

        return None

    def find_by_id(self, sphere_id: str) -> object or None:
        """Search for a sphere by id and return sphere object if found"""
        return self.spheres[sphere_id]


class Sphere:
    """Represents a Sphere"""

    def __init__(self, loop: asyncio.AbstractEventLoop, data: dict, user_id: str):
        self.loop = loop
        self.data = data
        self.user_id = user_id
        self.crownstones = Crownstones(loop, self.cloud_id)
        self.locations = Locations(loop, self.cloud_id)
        self.users = Users(loop, self.cloud_id)
        self.keys: dict = {}
        self.present_people = []

    @property
    def name(self) -> str:
        return self.data['name']

    @property
    def cloud_id(self) -> str:
        return self.data['id']

    @property
    def unique_id(self) -> int:
        return self.data['uid']

    async def get_keys(self) -> dict:
        """Async get the user keys for this sphere, that can be used for BLE (optional)"""
        keys = await RequestHandler.get('users', 'keysV2', model_id=self.user_id)
        for key_set in keys:
            if key_set['sphereId'] == self.cloud_id:
                for keyType in key_set['sphereKeys']:
                    self.keys[keyType['keyType']] = keyType['key']

        return self.keys

    def get_keys_sync(self) -> dict:
        """Sync get the user keys for this sphere, that can be used for BLE (optional)"""
        return self.loop.run_until_complete(self.get_keys())

    async def update_sphere_presence(self) -> None:
        """Replaces the current presence with that of the cloud."""
        presence_data = await RequestHandler.get('Spheres', 'presentPeople', model_id=self.cloud_id)
        for user in presence_data:
            self.present_people.append(user['userId'])