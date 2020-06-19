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

Synopsis: GRENML controller to track and organize top-level objects in a 
GRENML model/document.
"""
from grenml.models import Topology, Institution, Node,  Link, meta
from grenml.models import INSTITUTIONS, NODES, LINKS
from grenml.validation import TopologyValidator
from grenml.write import GRENMLWriter


class GRENMLManager:
    """
    Controller to manage GRENML objects at the top level of the
    hierarchy, such as Topologies, Lifetimes, Locations, Institutions.
    When importing or exporting XML, the objects at this level are
    contained in a top-level "namespace" element.
    """

    def __init__(self, name=None, validator=TopologyValidator(), writer=GRENMLWriter, *args, **kwargs):
        self._topology = Topology(name=name, *args, **kwargs)
        self._writer = writer(self)
        self._validator = validator
        self._validator.topology = self._topology

    @property
    def topology(self):
        return self._topology

    @property
    def writer(self):
        return self._writer

    def set_primary_owner(self, institution_id):
        self.topology.primary_owner = institution_id

    def add_institution(
            self, id=None, name=None, short_name=None, institution_type=None, longitude=None,
            latitude=None, altitude=None, unlocode=None, address=None, version=None,
            primary_owner=False, **kwargs
    ):
        """
        Adds a new institution to the topology. If the first argument is an
        institution, add that directly,
        otherwise take the arguments and create a new institution from that.
        """
        if id and isinstance(id, meta.GRENMLObject):
            inst = id
        else:
            inst = Institution(
                id, name, short_name, institution_type,
                longitude, latitude, altitude, unlocode, address, version,
                **kwargs
            )
        self.topology.add_institution(inst)
        if primary_owner:
            self.topology.primary_owner = inst
        return inst.id

    def add_institutions(self, institutions):
        """
        Take a list of potential institution objects and create their
        respective institutions.
        :param institutions: An Iterable that contains iterables, dictionaries,
        and/or Institutions to be
            added to the Topology.
        """
        ids = []
        for institution in institutions:
            if type(institution) in (list, set, tuple):
                ids.append(self.add_institution(*institution))
            elif type(institution) == dict:
                ids.append(self.add_institution(**institution))
            else:
                ids.append(self.add_institution(institution))
        return ids

    def get_institution(self, **kwargs):
        return self.topology.get_element(INSTITUTIONS, **kwargs)

    def get_institutions(self, **kwargs):
        return self.topology.get_elements(INSTITUTIONS, **kwargs)

    def delete_institutions(self, **kwargs):
        """
        Collects a list of institutions based on criteria and deletes them all
        """
        institutions = self.get_institutions(**kwargs)
        self.topology.delete_elements(INSTITUTIONS, institutions)

    def add_node(
            self, id=None, name=None, short_name=None, owners=None,
            longitude=None, latitude=None, altitude=None, unlocode=None, address=None,
            lifetime_start=None, lifetime_end=None,
            version=None, **kwargs
    ):
        if id and isinstance(id, meta.GRENMLObject):
            node = id
        else:
            node = Node(
                id=id, name=name, short_name=short_name, owners=owners,
                longitude=longitude, latitude=latitude, altitude=altitude, unlocode=unlocode, address=address,
                lifetime_start=lifetime_start, lifetime_end=lifetime_end, version=version,
                **kwargs
            )

        owners = []
        for owner in node.owners:
            if isinstance(owner, meta.GRENMLObject):
                owners.append(owner.id)
            else:
                owners.append(str(owner))
        node.owners = owners

        self.topology.add_node(node)
        return node.id

    def add_nodes(self, nodes):
        ids = []
        for node in nodes:
            if type(node) in (list, set, tuple):
                ids.append(self.add_node(*node))
            elif type(node) == dict:
                ids.append(self.add_node(**node))
            else:
                ids.append(self.add_node(node))
        return ids

    def get_node(self, **kwargs):
        return self.topology.get_element(NODES, **kwargs)

    def get_nodes(self, **kwargs):
        return self.topology.get_elements(NODES, **kwargs)

    def add_owner_to_node(self, owner_id, node_id):
        self.topology.get_element(NODES, id=node_id)._owners.add(owner_id)

    def remove_owner_from_node(self, owner_id, node_id):
        self.topology.get_element(NODES, id=node_id)._owners.remove(owner_id)

    def delete_nodes(self, **kwargs):
        nodes = self.get_nodes(**kwargs)
        self.topology.delete_elements(NODES, nodes)

    def add_link(
            self, id=None, name=None, short_name=None, owners=None, nodes=None,
            lifetime_start=None, lifetime_end=None, version=None, **kwargs
    ):
        if isinstance(id, meta.GRENMLObject):
            link = id
        else:
            link = Link(
                id=id, name=name, short_name=short_name, owners=owners, nodes=nodes,
                lifetime_start=lifetime_start, lifetime_end=lifetime_end, version=version,
                **kwargs
            )

        owners = []
        for owner in link.owners:
            if isinstance(owner, meta.GRENMLObject):
                owners.append(owner.id)
            else:
                owners.append(str(owner))

        nodes = []
        for node in link.nodes:
            if isinstance(node, meta.GRENMLObject):
                nodes.append(node.id)
            else:
                nodes.append(str(node))
        link.nodes = nodes
        link.owners = owners

        self.topology.add_link(link)
        return link.id

    def add_links(self, links):
        ids = []
        for link in links:
            if type(link) == list:
                ids.append(self.add_link(*link))
            elif type(link) == dict:
                ids.append(self.add_link(**link))
            else:
                ids.append(self.add_link(link))
        return ids

    def get_link(self, **kwargs):
        return self.topology.get_element(LINKS, **kwargs)

    def get_links(self, **kwargs):
        return self.topology.get_elements(LINKS, **kwargs)

    def add_owner_to_link(self, owner_id, link_id):
        self.topology.get_element(LINKS, id=link_id)._owners.add(owner_id)

    def remove_owner_from_link(self, owner_id, link_id):
        self.topology.get_element(LINKS, id=link_id)._owners.remove(owner_id)

    def delete_links(self, **kwargs):
        links = self.get_links(**kwargs)
        self.topology.delete_elements(LINKS, links)

    def write_to_file(self, filename):
        self.validate()
        self.writer.write_file(filename)

    def write_to_output_stream(self, stream):
        self.validate()
        self.writer.write_stream(stream)

    def write_to_string(self):
        self.validate()
        return self.writer.write_string()

    def validate(self, raise_error=True):
        return self._validator.validate(raise_error=raise_error)
