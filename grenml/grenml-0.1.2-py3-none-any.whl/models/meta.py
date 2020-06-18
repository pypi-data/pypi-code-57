"""
Copyright 2020 CANARIE Inc.

SPDX-License-Identifier: Apache License 2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

--------------------------------------------------------------------

Synopsis: Base objects used by the model classes to cover common fields
"""

from uuid import uuid4 as uuid
from grenml.exceptions import AttributeIdError, AttributeLongitudeError
from grenml.exceptions import AttributeLatitudeError
from collections.abc import Iterable
from datetime import datetime
from dateutil.tz import tzlocal
from backports.datetime_fromisoformat import MonkeyPatch
MonkeyPatch.patch_fromisoformat()


def add_to_list(obj, item):
    if isinstance(obj, Iterable) and not type(obj) == str:
        if isinstance(obj, list):
            if isinstance(item, Iterable) and not isinstance(item, str):
                obj += list(item)
            else:
                obj.append(item)
        elif isinstance(obj, set):
            obj.add(item)
    elif obj:
        obj = [obj, ]
        if isinstance(item, Iterable) and not isinstance(item, str):
            obj += list(item)
        else:
            obj.append(item)
    else:
        if isinstance(item, Iterable) and not isinstance(item, str):
            obj = list(item)
        else:
            obj = [item]
    return obj


def remove_from_list(obj, item):
    if isinstance(obj, Iterable) and not type(obj) == str:
        obj.remove(item)
        return obj
    elif obj != item and item:
        raise KeyError()
    else:
        return None


def convert_to_full_iso_format(iso_string):
    if 'Z' == iso_string[-1]:
        iso_string = iso_string.replace('Z', '+00:00')
    iso_string = datetime.fromisoformat(iso_string).replace(microsecond=0)
    if iso_string.tzinfo is None:
        iso_string = iso_string.replace(tzinfo=tzlocal())
    iso_string = iso_string.isoformat()
    return iso_string


def convert_datetime_to_iso_string(value):
    if isinstance(value, str):
        value = convert_to_full_iso_format(value)
    elif isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(microsecond=0, tzinfo=tzlocal()).isoformat()
        else:
            value = value.replace(microsecond=0).isoformat()
    elif isinstance(value, int):
        value = datetime.fromtimestamp(value).replace(tzinfo=tzlocal(), microsecond=0).isoformat()
    elif value is not None:
        raise ValueError('Invalid datetime format')
    if value:
        value = str(value)
    return value


class GRENMLObject:

    _id = None
    _name = None
    _parent = None
    _version = None
    _short_name = None

    def __init__(
        self, id=None, name=None,
        short_name=None, version=None, *args, **kwargs
    ):
        if not id:
            id = str(uuid())
        self.id = id
        self.name = name
        self.short_name = short_name
        self.version = version
        self._properties = {}

        for key, value in kwargs.items():
            self.add_property(key, value)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if not id:
            raise AttributeIdError()
        self._id = str(id)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, version):
        self._version = convert_datetime_to_iso_string(version)

    @property
    def short_name(self):
        return self._short_name

    @short_name.setter
    def short_name(self, short_name):
        self._short_name = short_name

    @property
    def additional_properties(self):
        return self._properties

    def add_property(self, attr, value):
        got_attr = self._properties.get(attr, None)
        got_attr = add_to_list(got_attr, value)
        self._properties[attr] = got_attr

    def del_property(self, attr, value=None):
        if not value:
            self._properties.pop(attr)
            return
        got_attr = self._properties[attr]
        got_attr = remove_from_list(got_attr, value)
        if not got_attr:
            self._properties.pop(attr)
        else:
            self._properties[attr] = got_attr

    def match(self, **kwargs):
        """
        Perform a look up of all keyword arguments and compare them to the
        attributes of this object.
        Supports the ability of 'loose' look up using the arguments with
        extensions.
        Extension options:
        __in: Look up to see if the attribute value is in the argument.
            Examples:
                id__in=['Test id', '23254:5niof:42noiaiw:fse', 'TEST ID 2']
                will compare the ID to each entry in the list.
                id__in='TEST4378943TEST_ID_1_CAN' will check if the ID
                is a substring of the argument.
                owners__in=['test_id_1', 'test_id_2', 'test_id_3'] If owners
                is a list, evaluate that owners is
                    a sublist of the argument provided
        __contains: Look up to see if the attribute value contains the argument
            Examples:
                id__contains='CAN' will check for any ID containing
                the string CAN
                owners__contains=['test_id_1', 'test_id_2'] If owners is a
                list, evaluate that the attribute contains all
                    the values in the provided argument

        Example Uses:
        match(id__contains='CAN', name='TEST') will return True if the ID
        contains 'CAN' and the name is 'TEST'
        match(id__in=['CAN_1', 'TEST', 'TEST 2'] name__contains='TEST_') will
        return True if the ID is in the given list
            and the name contains the string 'TEST_' in it.
        match(owners__contains='CAN_1') will match if ID 'CAN_1'
        is in the owners list.
        :return: If all provided values given match, return True, else False.
        """
        for param, search_value in kwargs.items():
            # key of property to check in the source object
            key = param.split('__')[0]
            # Value of the property being checked in the source object
            value = getattr(self, key, None)
            # If an operation is specified on the match, use it here
            if '__' in param:
                # The desired option for match
                option = param.split('__')[-1]
                if option == 'contains':
                    if isinstance(search_value, Iterable) and not type(search_value) == str:
                        if not (set(search_value).issubset(value) and search_value):
                            return False
                    else:
                        if search_value not in value:
                            return False
                elif option == 'in':
                    if isinstance(value, Iterable) and not type(value) == str:
                        if not (set(search_value).issuperset(value) and value):
                            return False
                    else:
                        if value not in search_value:
                            return False
            else:
                if isinstance(value, Iterable) and not type(value) == str:
                    if set(value) != set(search_value):
                        return False
                elif value != search_value:
                    return False
        return True

    def __eq__(self, other):
        """
        Dynamically evaluate that all attributes in this object and the other object match or, if given a string, that
        the string matches the ID of the object.
        :param other: The object being equated to
        :return: If all attributes and their values between the this object and the other object match,
            or the given string matches the ID, then return true, else false.
        """
        if not isinstance(other, (type(self), str)):
            return False
        elif isinstance(other, str):
            return other == self.id
        for attr in dir(self):
            value_self = getattr(self, attr, None)
            value_other = getattr(other, attr, None)
            if '_' in attr or callable(value_self):
                continue
            if isinstance(value_self, Iterable) and not isinstance(value_self, str):
                if set(value_self) != set(value_other):
                    return False
            elif value_self != value_other:
                return False
        return True

    def __hash__(self):
        """
        Have the ID hashable so sets can appropriately compare
        lists of objects to lists of IDs.
        """
        return hash(self.id)


class Location:
    """
    A representation of a location for the purposes of
    being displayed on a map.
    A location can be a city, PoP,
    """

    def __init__(
        self, longitude, latitude, altitude=None,
        unlocode=None, address=None, **kwargs
    ):
        super().__init__(**kwargs)
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = altitude
        self.unlocode = unlocode
        self._addresses = []
        if address is not None:
            if type(address) == str:
                self.address = address
            elif isinstance(address, Iterable):
                self.addresses = address

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, longitude):
        if longitude is None:
            self._longitude = longitude
        elif -180 <= float(longitude) <= 180:
            self._longitude = float(longitude)
        else:
            raise AttributeLongitudeError

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, latitude):
        if latitude is None:
            self._latitude = latitude
        elif -90 <= float(latitude) <= 90:
            self._latitude = float(latitude)
        else:
            raise AttributeLatitudeError

    @property
    def altitude(self):
        return self._altitude

    @altitude.setter
    def altitude(self, altitude):
        self._altitude = altitude

    @property
    def unlocode(self):
        return self._unlocode

    @unlocode.setter
    def unlocode(self, unlocode):
        self._unlocode = unlocode

    @property
    def address(self):
        return self.addresses[0] if len(self.addresses) > 0 else None

    @address.setter
    def address(self, address):
        if len(self.addresses) == 0:
            self.addresses.append(address)
        else:
            self.addresses[0] = address

    @address.deleter
    def address(self):
        self.addresses[0] = None

    @property
    def addresses(self):
        return self._addresses

    @addresses.setter
    def addresses(self, addresses):
        self._addresses = addresses

    @addresses.deleter
    def addresses(self):
        self._addresses = []

    def add_address(self, address):
        self.addresses.append(address)

    def remove_address(self, address):
        self.addresses.remove(address)


class Lifetime:
    """
    Represent a Lifetime of an Object. This can be used to represent
    situations such as the timeline of a contract.
    If a end value is given to the Lifetime, there must be a value
    in the start attribute.
    All Date values should be in ISO format.
    """

    def __init__(self, lifetime_start=None, lifetime_end=None, **kwargs):
        super().__init__(**kwargs)
        self.lifetime_start = lifetime_start
        self.lifetime_end = lifetime_end

    @property
    def lifetime_start(self):
        return self._lifetime_start

    @lifetime_start.setter
    def lifetime_start(self, start):
        self._lifetime_start = convert_datetime_to_iso_string(start)

    @property
    def lifetime_end(self):
        return self._lifetime_end

    @lifetime_end.setter
    def lifetime_end(self, end):
        self._lifetime_end = convert_datetime_to_iso_string(end)
