"""Location handler for Crownstone cloud data."""
from crownstone_cloud._RequestHandlerInstance import RequestHandler
import asyncio


class Locations:
    """Handler for the locations of a sphere."""

    def __init__(self, loop: asyncio.AbstractEventLoop, sphere_id: str) -> None:
        """Initialization."""
        self.loop = loop
        self.locations = {}
        self.sphere_id = sphere_id

    def __iter__(self):
        """Iterate over locations."""
        return iter(self.locations.values())

    async def async_update_location_data(self) -> None:
        """
        Get the locations and presence from the cloud.

        This method is a coroutine.
        """
        location_data = await RequestHandler.get(
            'Spheres', 'ownedLocations', model_id=self.sphere_id
        )
        # process items
        removed_items = []
        new_items = []
        for location in location_data:
            location_id = location['id']
            exists = self.locations.get(location_id)
            # check if the location already exists
            # it is important that we don't throw away existing objects, as they need to remain functional
            if exists:
                # update data
                self.locations[location_id].data = location
            else:
                # add new Location
                self.locations[location_id] = Location(location)

            # generate list with new id's to check with the existing id's
            new_items.append(location_id)

        # check for removed items
        for location_id in self.locations:
            if location_id not in new_items:
                removed_items.append(location_id)

        # remove items from dict
        for location_id in removed_items:
            del self.locations[location_id]

    async def async_update_location_presence(self) -> None:
        """
        Get the presentPeople for this Sphere, and get the users in this Location.

        This method is a coroutine.
        """
        presence_data = await RequestHandler.get(
            'Spheres', 'presentPeople', model_id=self.sphere_id
        )
        # reset the presence
        for location in self.locations.values():
            location.present_people = []
        # add new presence
        for presence in presence_data:
            for present_location in presence['locations']:
                for location in self.locations.values():
                    if present_location == location.cloud_id:
                        location.present_people.append(presence['userId'])

    def update_location_data(self) -> None:
        """Update the location data."""
        self.loop.run_until_complete(self.async_update_location_data())

    def find(self, location_name: str) -> object or None:
        """Search for a sphere by name and return sphere object if found."""
        for location in self.locations.values():
            if location_name == location.name:
                return location

        return None

    def find_by_id(self, location_id: str) -> object or None:
        """Search for a sphere by id and return sphere object if found."""
        return self.locations[location_id]


class Location:
    """Represents a Location."""

    def __init__(self, data: dict):
        """Initialization."""
        self.data = data
        self.present_people = []

    @property
    def name(self) -> str:
        """Return the name of this Location."""
        return self.data['name']

    @property
    def cloud_id(self) -> str:
        """Return the cloud id of this Location."""
        return self.data['id']

    @property
    def unique_id(self) -> int:
        """Return the unique id of this Location."""
        return self.data['uid']
