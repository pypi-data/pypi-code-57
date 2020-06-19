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

Synopsis: A validation class to evaluate that the supplied Topology object contains expected data format
"""
from collections.abc import Iterable

from grenml.models import Topology, Institution, Node, Link, GLOBAL_INSTITUTION_ID
from grenml.models.meta import GRENMLObject, Location, Lifetime
from re import match

ISO_FORMAT = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[-+]\d{2}:\d{2}'


class TopologyValidator:
    """
    The validation class made to validate a Topology
    """

    def __init__(self):
        self._topology = None

    @property
    def topology(self):
        return self._topology

    @topology.setter
    def topology(self, topology):
        if not isinstance(topology, Topology):
            raise ValueError('The Validator must be passed a Topology object')
        self._topology = topology

    @property
    def is_valid(self):
        errors = self.validate(self.topology, raise_error=False)
        for error in errors:
            print(error)
        return not bool(errors)

    def validate(self, topology=None, raise_error=True):
        if not topology and self.topology:
            topology = self.topology
        errors = self._validate_topology(topology)
        if errors and raise_error:
            raise ValueError('\n'.join(errors))
        return errors

    def _validate_topology(self, topology: Topology, parent=None):
        """
        Validate that the topology provided meets the XSD standards.
        A topology must have the following:
         - It must meet object default standards.
         - It must have a Primary owner assigned
         - It must have its primary owner in its institution list
         - It must have the global institution in the institution list
        :param topology: The topology being evaluated
        :param parent: The Parent Topology. If this topology is the top level, then the parent should be None.
        :return: A list of any issues in the data.
        """
        errors = []
        errors += self._validate_object_defaults(topology, parent)
        if not topology.primary_owner:
            errors.append('Topology {} ID: {} must have a primary owner'.format(topology.name, topology.id))
        elif topology.primary_owner not in topology.institutions:
            errors.append(
                'Topology {} ID: {} primary owner ID {} must be in the Topologies Institutions'.format(
                    topology.name, topology.id, topology.primary_owner,
                )
            )
        if not topology._parent == parent:
            errors.append(
                'Topology {} parent topology does not match. {} != {}'.format(
                    topology.id, topology._parent, parent
                )
            )
        if GLOBAL_INSTITUTION_ID not in topology.institutions:
            errors.append('Global Institution must be in Topology {}'.format(topology.id))
        for inst in topology.institutions:
            errors += self._validate_institution(inst, topology)
        for node in topology.nodes:
            errors += self._validate_node(node, topology)
        for link in topology.links:
            errors += self._validate_link(link, topology)
        for sub_topology in topology.topologies:
            errors += self._validate_topology(sub_topology, topology)
        return errors

    def _validate_institution(self, institution: Institution, topology: Topology):
        """
        Validate that the institution provided meets the XSD standards.
        A institution must have the following:
         - It must meet object default standards.
         - It's Location values are valid
         - The Institution Type must be in the list of valid Institution types
        :param institution: The Institution being evaluated.
        :param topology: The Parent Topology.
        :return: A list of any issues in the data.
        """
        errors = []
        errors += self._validate_object_defaults(institution, topology)
        errors += self._validate_location(institution, False)
        if not institution.type:
            errors.append(
                'Institution {} must have a set type. '.format(
                    institution.id
                )
            )
        return errors

    def _validate_node(self, node: Node, topology: Topology):
        """
        Validate that the node provided meets the XSD standards.
        A node must have the following:
         - It must meet object default standards.
         - It's Location values are valid
         - It's Lifetime values are valid
         - All owners in the node must be strings
         - All owners in the node must be IDs for an institution in the parent topologies institution list
         - The node must have its parent Topology's primary owner in its list of owners
        :param node: The Node being evaluated.
        :param topology: The Parent Topology.
        :return: A list of any issues in the data.
        """
        errors = []
        errors += self._validate_object_defaults(node, topology)
        errors += self._validate_location(node)
        errors += self._validate_lifetime(node)
        for owner in node._owners:
            if not isinstance(owner, str):
                errors.append(
                    'Node {} owner {} should be a string. Not {}'.format(
                        node.id, owner, owner.__class__.__name__
                    )
                )
            if topology and owner not in topology.institutions:
                errors.append(
                    'Node {} listed owner id {} does not exist in parent Topology {}'.format(
                        node.id, owner, topology.id
                    )
                )
        if topology and topology.primary_owner not in node.owners:
            errors.append(
                'Node {} does not have the Topology primary owner {} in its list of owners'.format(
                    node.id, topology.primary_owner
                )
            )
        return errors

    def _validate_link(self, link: Link, topology: Topology):
        """
        Validate that the link provided meets the XSD standards.
        A link must have the following:
         - It must meet object default standards.
         - It's Lifetime values are valid
         - All owners in the link must be strings
         - All owners in the link must be IDs for an institution in the parent topologies institution list
         - The link must have its parent Topology's primary owner in its list of owners
         - A link can only connect to 2 nodes
         - The nodes that a link is connected to must be in the parent Topology's nodes list
        :param link: The Link being evaluated.
        :param topology: The Parent Topology.
        :return: A list of any issues in the data.
        """
        errors = []
        errors += self._validate_object_defaults(link, topology)
        errors += self._validate_lifetime(link)
        for owner in link._owners:
            if not isinstance(owner, str):
                errors.append(
                    'Link {} owner {} should be a string. Not {}'.format(
                        link.id, owner, owner.__class__.__name__
                    )
                )
            if topology and owner not in topology.institutions:
                errors.append(
                    'Link {} listed owner id {} does not exist in parent Topology {}'.format(
                        link.id, owner, topology.id
                    )
                )
        if topology and topology.primary_owner not in link.owners:
            errors.append(
                'Link {} does not have the Topology primary owner {} in its list of owners'.format(
                    link.id, topology.primary_owner
                )
            )
        if len(link._nodes) != 2:
            errors.append(
                'Link {} must connect between 2 Nodes. Currently {}'.format(
                    link.id, str(link._nodes)
                )
            )
        for node in link._nodes:
            if not isinstance(node, str):
                errors.append(
                    'Link {} Node {} should be a string. Not {}'.format(
                        link.id, node, node.__class__.__name__
                    )
                )
            if topology and node not in topology.nodes:
                errors.append(
                    'Link {} listed node id {} does not exist in parent Topology {}'.format(
                        link.id, node, topology.id
                    )
                )
        return errors

    def _validate_object_defaults(self, grenml_object: GRENMLObject, parent: GRENMLObject):
        """
        Validate that the object provided default fields meets the XSD standards.
        The object must have the following:
         - The object must have an ID
         - The object ID must be a string
         - The object must have a name
         - The object name must be a string
         - If the object has a short name, it must be a string
         - If the object has a version, it must be a string in ISO format
         - The object's parent must be the provided parent Topology
         - All the additional properties on the object are proper
        :param grenml_object: The GRENML Model Object being evaluated.
        :param topology: The Parent Topology.
        :return: A list of any issues in the data.
        """
        errors = []
        if not grenml_object.id:
            errors.append('{} must have an ID'.format(grenml_object.__class__.__name__))
        if not isinstance(grenml_object.id, str):
            errors.append('{} ID must be a string'.format(grenml_object.__class__.__name__))
        if not grenml_object.name:
            errors.append(
                '{} {} must have a name'.format(
                    grenml_object.__class__.__name__, grenml_object.id,
                )
            )
        if not isinstance(grenml_object.name, str):
            errors.append(
                '{} {} name must be a String'.format(
                    grenml_object.__class__.__name__, grenml_object.id,
                )
            )
        if grenml_object.short_name:
            if not isinstance(grenml_object.short_name, str):
                errors.append(
                    '{} {} Short name must be a string'.format(
                        grenml_object.__class__.__name__, grenml_object.id,
                    )
                )
        if grenml_object.version:
            if not isinstance(grenml_object.version, str):
                errors.append(
                    '{} {} Version must be a String'.format(
                        grenml_object.__class__.__name__, grenml_object.id,
                    )
                )
            elif not match(ISO_FORMAT, grenml_object.version):
                errors.append(
                    '{} {} Version must be datetime ISO format'.format(
                        grenml_object.__class__.__name__, grenml_object.id,
                    )
                )
        if grenml_object._parent != parent:
            errors.append(
                '{} {} parent does not match the topology it is in. {} != {}'.format(
                    grenml_object.__class__.__name__, grenml_object.id, grenml_object._parent, parent
                )
            )

        errors += self._validate_additional_properties(grenml_object)
        return errors

    def _validate_additional_properties(self, grenml_object: GRENMLObject):
        """
        Validate that the object additional properties meets the XSD standards.
        The additional properties must have the following:
         - The property key must be a string
         - The property value must be an iterable, non-dictionary, value
         - Each entry in the property value must be a raw value
        :param grenml_object: The GRENML Model Object being evaluated.
        :return: A list of any issues in the data.
        """
        errors = []
        for key, values in grenml_object.additional_properties.items():
            if not isinstance(key, str):
                errors.append(
                    '{} {} Property key {} must be a string value'.format(
                        grenml_object.__class__.__name__, grenml_object.id, str(key),
                    )
                )
            if not isinstance(values, Iterable) or isinstance(values, (str, dict)):
                errors.append(
                    '{} {} Property {} must be a non-dictionary iterable'.format(
                        grenml_object.__class__.__name__, grenml_object.id, key,
                    )
                )
            else:
                for value in values:
                    if not isinstance(value, (int, float, str, bool)):
                        errors.append(
                            '{} {} Property {} Value {} should be a raw value.'.format(
                                grenml_object.__class__.__name__, grenml_object.id, key, value
                            )
                        )
        return errors

    def _validate_location(self, location: Location, enforce_coordinates=True):
        """
        Validate that the object location fields meets the XSD standards.
        The location must have the following:
         - A location must have a longitude
         - A location's longitude muse be a floating point value
         - A location's longitude must be between -180 and -180
         - A location must have a latitude
         - A location must be a floating point value
         - A location's latitude must be between -90 and 90
         - A location's altitude must be a floating point value
         - A location's UN/LOCODE must be a string value
         - A location's address must be a string or a list of strings
        :param location: The Location Object being evaluated.
        :param enforce_coordinates: A boolean determining if longitude and latitude should be enforced
        :return: A list of any issues in the data.
        """
        errors = []
        if location.longitude is None and enforce_coordinates:
            errors.append(
                '{} {} Longitude must be set to a value'.format(
                    location.__class__.__name__, location.id,
                )
            )
        try:
            if location.longitude is not None:
                if not -180 <= float(location.longitude) <= 180:
                    errors.append(
                        '{} {} Longitude must be a value that is between -180 and 180'.format(
                            location.__class__.__name__, location.id,
                        )
                    )
        except ValueError:
            errors.append(
                '{} {} Longitude must be a value that coordinates to a Floating point value'.format(
                    location.__class__.__name__, location.id,
                )
            )

        if location.latitude is None and enforce_coordinates:
            errors.append(
                '{} {} Latitude must be set to a value'.format(
                    location.__class__.__name__, location.id
                )
            )
        try:
            if location.latitude is not None:
                if not -90 <= float(location.latitude) <= 90:
                    errors.append(
                        '{} {} Latitude must be a value that is between -90 and 90'.format(
                            location.__class__.__name__, location.id,
                        )
                    )
        except ValueError:
            errors.append(
                '{} {} Latitude must be a value that coordinates to a Floating point value'.format(
                    location.__class__.__name__, location.id,
                )
            )

        try:
            if location.altitude:
                float(location.altitude)
        except ValueError:
            errors.append(
                '{} {} Altitude must be a value that coordinates to a Floating point value'.format(
                    location.__class__.__name__, location.id,
                )
            )

        if location.unlocode and not isinstance(location.unlocode, str):
            errors.append(
                '{} {} UN/LOCODE must be a string value'.format(location.__class__.__name__, location.id)
            )
        if isinstance(location.addresses, Iterable):
            for address in location.addresses:
                if not type(address) == str:
                    errors.append(
                        '{} {} Address {} must be a string'.format(
                            location.__class__.__name__, location.id, address
                        )
                    )
        else:
            errors.append(
                '{} {} Addresses should be a list of strings'.format(
                    location.__class__.__name__, location.id
                )
            )
        return errors

    def _validate_lifetime(self, lifetime: Lifetime):
        """
        Validate that the object lifetime fields meets the XSD standards.
        The lifetime must have the following:
         - If a lifetime has an end value, it must have a start value
         - The lifetime's start time must be a string and match the ISO format, if it exists
         - The lifetime's end time must be a string and match the ISO format, if it exists
        :param lifetime: The Lifetime Object being evaluated.
        :return: A list of any issues in the data.
        """
        errors = []
        if not lifetime.lifetime_start and lifetime.lifetime_end:
            errors.append(
                '{} {} Lifetime needs a start datetime if given an end datetime'.format(
                    lifetime.__class__.__name__, lifetime.id,
                )
            )
        if lifetime.lifetime_start and not match(ISO_FORMAT, lifetime.lifetime_start):
            errors.append(
                '{} {} Lifetime Start needs to be in full ISO format'.format(
                    lifetime.__class__.__name__, lifetime.id,
                )
            )
        if lifetime.lifetime_end and not match(ISO_FORMAT, lifetime.lifetime_end):
            errors.append(
                '{} {} Lifetime End needs to be in full ISO format'.format(
                    lifetime.__class__.__name__, lifetime.id,
                )
            )
        return errors
