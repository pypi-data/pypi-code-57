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

Synopsis: The representation of an institution in the GRENML topology
"""
from .meta import GRENMLObject, Location, add_to_list

# This is a recommended list of Institution Types. This is DEPRECATED and will be removed at a later date.
INSTITUTION_TYPES = [
    'pren', 'nren', 'sren', 'connected institution', 'global', 'other',
]


class Institution(Location, GRENMLObject):
    """
    Represents a connected institution or a REN
    (Research and Education Network)
    or any other organisation entity. Frequently used to represent "ownership"
    of NetworkObjects, as in "Link A belongs to NREN X and RREN Y".
    """

    def __init__(
            self, id=None, name=None, short_name=None, institution_type=None,
            longitude=None, latitude=None, altitude=None, unlocode=None, address=None,
            version=None, **kwargs
    ):
        super().__init__(
            id=id, name=name, short_name=short_name, longitude=longitude, latitude=latitude,
            altitude=altitude, unlocode=unlocode, address=address, version=version,
            **kwargs
        )
        self.type = institution_type

    @property
    def type(self):
        return self._type[0] if self._type else None

    @type.setter
    def type(self, type):
        if type:
            self._type = add_to_list(None, type)
        else:
            self._type = []

    @property
    def types(self):
        return self._type
