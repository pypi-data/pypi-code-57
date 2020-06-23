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

Synopsis: The representation of a Node in the GRENML topology
"""
from .meta import GRENMLObject, Location, Lifetime
from .topologies import INSTITUTIONS


class Node(Location, Lifetime, GRENMLObject):
    """
    GRENML NetworkObject representing a network node
    """

    def __init__(
            self, id=None, name=None, short_name=None, owners=None,
            longitude=None, latitude=None, altitude=None, unlocode=None, address=None,
            lifetime_start=None, lifetime_end=None,
            version=None, **kwargs):
        super().__init__(
            id=id, name=name, short_name=short_name, longitude=longitude, latitude=latitude,
            altitude=altitude, unlocode=unlocode, address=address, version=version,
            lifetime_start=lifetime_start, lifetime_end=lifetime_end,
            **kwargs
        )
        self.owners = owners

    @property
    def owners(self):
        if self._parent:
            return self._parent.get_elements(
                INSTITUTIONS, id__in=self._owners
            ) or set()
        else:
            return self._owners

    @owners.setter
    def owners(self, owners):
        if not owners:
            owners = []
        self._owners = set(owners)

    @owners.deleter
    def owners(self):
        self.owners = set()
