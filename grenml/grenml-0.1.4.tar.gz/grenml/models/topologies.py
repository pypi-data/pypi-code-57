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

Synopsis: GRENML Topology NetworkObject representation.
"""
from .meta import GRENMLObject
from .institutions import Institution
from grenml.exceptions import InstitutionNotFoundError, NodeNotFoundError, \
    AttributeIdError, MultipleReturnedError, \
    LinkNotFoundError, TopologyNotFoundError
GLOBAL_INSTITUTION_ID = 'urn:ogf:networking:global'

INSTITUTIONS = 'institutions'
NODES = 'nodes'
LINKS = 'links'
TOPOLOGIES = 'topology'

EXCEPTIONS = {
    INSTITUTIONS: InstitutionNotFoundError,
    NODES: NodeNotFoundError,
    TOPOLOGIES: TopologyNotFoundError,
    LINKS: LinkNotFoundError,
}


class Topology(GRENMLObject):
    """
    Toplogy is an NML NetworkObject by definition.
    """

    def __init__(self, name=None, version=None, **kwargs):
        self._primary_owner = None
        self._elements = {
            INSTITUTIONS: set(),
            NODES: set(),
            TOPOLOGIES: set(),
            LINKS: set(),
        }
        global_institution = Institution(
            id=GLOBAL_INSTITUTION_ID, name='GREN', institution_type='global'
        )
        global_institution._parent = self
        self._elements[INSTITUTIONS].add(global_institution)
        super(Topology, self).__init__(name=name, version=version, **kwargs)

    @property
    def primary_owner(self):
        return self._primary_owner

    @primary_owner.setter
    def primary_owner(self, owner):
        if isinstance(owner, GRENMLObject):
            owner = owner.id
        self._primary_owner = owner

    @property
    def institutions(self):
        return self._elements[INSTITUTIONS]

    @property
    def nodes(self):
        return self._elements[NODES]

    @property
    def links(self):
        return self._elements[LINKS]

    @property
    def topologies(self):
        return self._elements[TOPOLOGIES]

    def add_institution(self, inst):
        self._add_element(INSTITUTIONS, inst)

    def add_node(self, node):
        if self.primary_owner and self.primary_owner not in node.owners:
            # Only works because the node shouldn't have a parent yet.
            node.owners.add(self.primary_owner)
        self._add_element(NODES, node)

    def add_link(self, link):
        if self.primary_owner and self.primary_owner not in link.owners:
            link.owners.add(self.primary_owner)
        self._add_element(LINKS, link)

    def add_topology(self, topology):
        self._add_element(TOPOLOGIES, topology)

    def _add_element(self, ele_type, element):
        if element.id in self._elements[ele_type]:
            raise AttributeIdError(
                '{} ID must be unique'.format(type(element).__name__)
            )
        element._parent = self
        self._elements[ele_type].add(element)

    def get_element(self, search_type=None, **kwargs):
        """
        Gets the first element that matches to the defined parameters.
        :return: The GRENObject object that matches the given parameters.
        :raises: ObjectNotFoundError: There is no element that matches the
        given parameters.
            A subclass of ObjectNotFoundError will be raised
        :raises: MultipleReturnedError: If the parameters match with multiple
        elements, rather than
            arbitrarily picking an element, raise this error.
        """
        try:
            elements = self.get_elements(search_type, **kwargs)
            if len(elements) > 1:
                raise MultipleReturnedError
            return elements.pop()
        except (AttributeError, TypeError):
            raise EXCEPTIONS[search_type]()

    def get_elements(self, search_type=None, **kwargs):
        """
        Collects all the elements in the topology that matches the given
        parameters
        :param search_type: The specific type of element to search against
        :param kwargs: The key word arguments to search against specific
        attributes
        :return: A list of GRENObjects that match the criteria, or None if
        none are found.
        """
        matches = []
        for element in self._elements[search_type]:
            if element.match(**kwargs):
                matches.append(element)
        return set(matches) or None

    def delete_elements(self, ele_type, elements):
        """
        Take a list of elements and delete them from the topology
        :param ele_type: The type of element to delete from
        :param elements: The elements to be removed.
        """
        for element in elements:
            self._elements[ele_type].remove(element)

    def update_elements_properties(
        self, element_type, match_kwargs,
        attr, value=None, append=False, remove=False
    ):

        if append and remove:
            raise ValueError(
                'Topology cannot add and remove a value at the same time.'
            )

        elements = self.get_elements(element_type, **match_kwargs)
        if not elements:
            raise EXCEPTIONS[element_type]()
        for element in elements:
            if append:
                element.add_property(attr, value)
            elif remove:
                element.del_property(attr, value)
            else:
                element.additional_properties[attr] = value
