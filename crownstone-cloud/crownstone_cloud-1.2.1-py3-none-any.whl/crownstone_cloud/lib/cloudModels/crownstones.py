"""Crownstone handler for Crownstone cloud data"""
from crownstone_cloud._RequestHandlerInstance import RequestHandler
from crownstone_cloud.const import (
    DIMMING_ABILITY
)
import logging
import asyncio

_LOGGER = logging.Logger(__name__)


class Crownstones:
    """Handler for the crownstones of a sphere."""

    def __init__(self, loop: asyncio.AbstractEventLoop, sphere_id: str) -> None:
        """Initialization."""
        self.loop = loop
        self.crownstones = {}
        self.sphere_id = sphere_id

    def __iter__(self):
        """Iterate over crownstones."""
        return iter(self.crownstones.values())

    async def async_update_crownstone_data(self) -> None:
        """Get the crownstones data from the cloud."""
        # include abilities and current switch state in the request
        data_filter = {"include": ["currentSwitchState", {"abilities": "properties"}]}
        # request data
        crownstone_data = await RequestHandler.get(
            'Spheres', 'ownedStones', filter=data_filter, model_id=self.sphere_id
        )
        # process items
        removed_items = []
        new_items = []
        for crownstone in crownstone_data:
            crownstone_id = crownstone['id']
            exists = self.crownstones.get(crownstone_id)
            # check if the crownstone already exists
            # it is important that we don't throw away existing objects, as they need to remain functional
            if exists:
                # update data and update abilities
                self.crownstones[crownstone_id].data = crownstone
            else:
                # add new Crownstone
                self.crownstones[crownstone_id] = Crownstone(self.loop, crownstone)

            # update the abilities of the Crownstone from the data
            self.crownstones[crownstone_id].update_abilities()

            # generate list with new id's to check with the existing id's
            new_items.append(crownstone_id)

        # check for removed items
        for crownstone_id in self.crownstones:
            if crownstone_id not in new_items:
                removed_items.append(crownstone_id)

        # remove items from dict
        for crownstone_id in removed_items:
            del self.crownstones[crownstone_id]

    def update_crownstone_data(self) -> None:
        """Sync function for updating the crownstone data."""
        self.loop.run_until_complete(self.async_update_crownstone_data())

    def find(self, crownstone_name: str) -> object or None:
        """Search for a crownstone by name and return crownstone object if found."""
        for crownstone in self.crownstones.values():
            if crownstone_name == crownstone.name:
                return crownstone

    def find_by_id(self, crownstone_id) -> object or None:
        """Search for a crownstone by id and return crownstone object if found."""
        return self.crownstones[crownstone_id]

    def find_by_uid(self, crownstone_uid) -> object or None:
        """Search for a crownstone by uid and return crownstone object if found."""
        for crownstone in self.crownstones.values():
            if crownstone_uid == crownstone.unique_id:
                return crownstone


class CrownstoneAbility:
    """Represents a Crownstone Ability"""

    def __init__(self, data: dict) -> None:
        """Initialization"""
        self.data = data
        self.is_enabled = self.data['enabled']
        self.properties = self.data['properties']

    @property
    def type(self) -> str:
        """Return the ability type."""
        return self.data['type']

    @property
    def ability_id(self) -> str:
        """Return the ability id."""
        return self.data['id']

    @property
    def crownstone_id(self) -> str:
        """Return the Crownstone id."""
        return self.data['stoneId']


class Crownstone:
    """Represents a Crownstone"""

    def __init__(self, loop: asyncio.AbstractEventLoop, data: dict) -> None:
        """Initialization."""
        self.loop = loop
        self.data = data
        self.abilities = {}

    @property
    def name(self) -> str:
        """Return the name of this Crownstone."""
        return self.data['name']

    @property
    def unique_id(self) -> int:
        """Return the unique_id of this Crownstone."""
        return self.data['uid']

    @property
    def cloud_id(self) -> str:
        """Return the cloud id of this Crownstone."""
        return self.data['id']

    @property
    def type(self) -> str:
        """Return the Crownstone type."""
        return self.data['type']

    @property
    def sw_version(self) -> str:
        """Return the firmware version of this Crownstone."""
        return self.data['firmwareVersion']

    @property
    def icon(self) -> str:
        """Return the icon of this Crownstone."""
        return self.data['icon']

    @property
    def state(self) -> float:
        """Return the last reported state for this Crownstone."""
        return self.data['currentSwitchState']['switchState']

    @state.setter
    def state(self, value: float) -> None:
        """Set a new state for this Crownstone."""
        self.data['currentSwitchState']['switchState'] = value

    def update_abilities(self) -> None:
        """Add/update the abilities for this Crownstone."""
        for ability in self.data['abilities']:
            self.abilities[ability['type']] = CrownstoneAbility(ability)

    async def async_turn_on(self) -> None:
        """
        Turn this crownstone on.

        This method is a coroutine.
        """
        await RequestHandler.put(
            'Stones', 'setSwitchStateRemotely', model_id=self.cloud_id, command='switchState', value=1
        )

    async def async_turn_off(self) -> None:
        """
        Turn this crownstone off.

        This method is a coroutine.
        """
        await RequestHandler.put(
            'Stones', 'setSwitchStateRemotely', model_id=self.cloud_id, command='switchState', value=0
        )

    async def async_set_brightness(self, brightness: float) -> None:
        """
        Set the brightness of this crownstone, if dimming enabled.

        :param brightness: brightness value between (0 - 1)

        This method is a coroutine.
        """
        if self.abilities[DIMMING_ABILITY].is_enabled:
            if brightness < 0 or brightness > 1:
                raise ValueError("Enter a value between 0 and 1")
            else:
                await RequestHandler.put(
                    'Stones', 'setSwitchStateRemotely', model_id=self.cloud_id, command='switchState', value=brightness
                )
        else:
            _LOGGER.warning("Dimming is not enabled for this crownstone. Go to the crownstone app to enable it")

    def turn_on(self) -> None:
        """Turn this Crownstone on."""
        self.loop.run_until_complete(self.async_turn_on())

    def turn_off(self) -> None:
        """Turn this Crownstone off."""
        self.loop.run_until_complete(self.async_turn_off())

    def set_brightness(self, brightness: float) -> None:
        """
        Set the brightness of this crownstone, if dimming enabled.

        :param brightness: the brightness value between (0 - 1)
        """
        self.loop.run_until_complete(self.async_set_brightness(brightness))
