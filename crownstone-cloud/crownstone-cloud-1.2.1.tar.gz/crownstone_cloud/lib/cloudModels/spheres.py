"""Sphere handler for Crownstone cloud data."""
from crownstone_cloud._RequestHandlerInstance import RequestHandler
from crownstone_cloud.lib.cloudModels.crownstones import Crownstones
from crownstone_cloud.lib.cloudModels.locations import Locations
from crownstone_cloud.lib.cloudModels.users import Users
import asyncio


class Spheres:
    """Handler for the spheres of the user."""

    def __init__(self, loop: asyncio.AbstractEventLoop, user_id: str) -> None:
        """Initialization."""
        self.loop = loop
        self.spheres = {}
        self.user_id = user_id

    def __iter__(self):
        """Iterate over spheres."""
        return iter(self.spheres.values())

    async def async_update_sphere_data(self) -> None:
        """
        Get the spheres for the user from the cloud.

        This method is a coroutine.
        """
        sphere_data = await RequestHandler.get(
            'users', 'spheres', model_id=self.user_id
        )
        # process items
        removed_items = []
        new_items = []
        for sphere in sphere_data:
            sphere_id = sphere['id']
            exists = self.spheres.get(sphere_id)
            # check if the Sphere already exists
            # it is important that we don't throw away existing objects, as they need to remain functional
            if exists:
                # update data
                self.spheres[sphere_id].data = sphere
            else:
                # add new Sphere
                self.spheres[sphere_id] = Sphere(self.loop, sphere, self.user_id)

            # generate list with new id's to check with the existing id's
            new_items.append(sphere_id)

        # check for removed items
        for sphere_id in self.spheres:
            if sphere_id not in new_items:
                removed_items.append(sphere_id)

        # remove items from dict
        for sphere_id in removed_items:
            del self.spheres[sphere_id]

    def update_sphere_data(self) -> None:
        """Get the sphere data from the cloud."""
        self.loop.run_until_complete(self.async_update_sphere_data())

    def find(self, sphere_name: str) -> object or None:
        """Search for a sphere by name and return sphere object if found."""
        for sphere in self.spheres.values():
            if sphere_name == sphere.name:
                return sphere

        return None

    def find_by_id(self, sphere_id: str) -> object or None:
        """Search for a sphere by id and return sphere object if found."""
        return self.spheres[sphere_id]


class Sphere:
    """Represents a Sphere"""

    def __init__(self, loop: asyncio.AbstractEventLoop, data: dict, user_id: str):
        """Initialization."""
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
        """Returns the name of this Sphere."""
        return self.data['name']

    @property
    def cloud_id(self) -> str:
        """Return the cloud id of this Sphere."""
        return self.data['id']

    @property
    def unique_id(self) -> int:
        """Return the unique id of this Sphere."""
        return self.data['uid']

    async def async_get_keys(self) -> dict:
        """
        Get the user keys for this sphere, that can be used for BLE (optional).

        This method is a coroutine.
        """
        keys = await RequestHandler.get('users', 'keysV2', model_id=self.user_id)
        for key_set in keys:
            if key_set['sphereId'] == self.cloud_id:
                for keyType in key_set['sphereKeys']:
                    self.keys[keyType['keyType']] = keyType['key']

        return self.keys

    async def async_update_sphere_presence(self) -> None:
        """
        Replaces the current presence with that of the cloud.

        This method is a coroutine.
        """
        self.present_people = []
        presence_data = await RequestHandler.get('Spheres', 'presentPeople', model_id=self.cloud_id)
        for user in presence_data:
            self.present_people.append(user['userId'])

    def get_keys(self) -> dict:
        """Get the user keys for this Sphere, that can be used for BLE (optional)."""
        return self.loop.run_until_complete(self.async_get_keys())
