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

Synopsis: A collection for Writer classes to produce XML
"""
from grenml.models.topologies import Topology
from grenml.models.institutions import Institution
from grenml.models.links import Link
from grenml.models.nodes import Node
from grenml.models.meta import GRENMLObject
from xml.sax.saxutils import XMLGenerator

GRENML_XMLNS_URI = 'http://schemas.ogf.org/nml/2020/01/grenml'
NML_XMLNS_URI = 'http://schemas.ogf.org/nml/2013/05/base#'
XSI_XMLNS_URI = 'http://www.w3.org/2001/XMLSchema-instance'
XSI_SCHEMA_LOCATION = 'http://schemas.ogf.org/nml/2020/01/grenml validation/grenml.xsd http://schemas.ogf.org/nml/2013/05/base# validation/nmlbase.xsd'


class Writer(XMLGenerator):
    """
    Base writer to provide capabilities to do basic xml writing
    """

    def __init__(self, stream):
        super().__init__(stream, 'utf-8')
        self.stream = stream

    def startElement(self, name, attrs={}):
        # Removes empty attributes
        attrs = {k: v for k, v in attrs.items() if v is not None}
        return super().startElement(name, attrs)

    def characters(self, content):
        return super().characters(str(content))

    def element(self, name, contents, attrs={}):
        """
        Helper function to write an element with contents if it has contents
        """
        if contents is not None:
            self.startElement(name, attrs)
            self.characters(contents)
            self.endElement(name)

    def write_properties(self, properties):
        """
        Writes the multiple property elements based on an array of properties
        """
        for name, values in properties.items():
            for value in values:
                self.element('grenml:Property', value, {'name': name})


class TopologyWriter(Writer):

    def __init__(self, stream, is_main=False):
        super().__init__(stream)
        self.is_main = is_main

    def write_element(self, topology: Topology):
        attributes = {'id': topology.id, 'topology': topology.version}
        if self.is_main:
            self.startDocument()
            attributes['xmlns:grenml'] = GRENML_XMLNS_URI
            attributes['xmlns:nml'] = NML_XMLNS_URI
            attributes['xmlns:xsi'] = XSI_XMLNS_URI
            attributes['xsi:schemaLocation'] = XSI_SCHEMA_LOCATION
        self.startElement('grenml:Topology', attributes)
        self.element('grenml:name', topology.name)
        self.element('grenml:owner', topology.primary_owner)
        self.write_properties(topology.additional_properties)
        for institution in topology.institutions:
            if not institution.id == 'global':
                InstitutionWriter(self.stream).write_element(institution)
        for link in topology.links:
            LinkWriter(self.stream).write_element(link)
        for node in topology.nodes:
            NodeWriter(self.stream).write_element(node)
        for topology in topology.topologies:
            TopologyWriter(self.stream).write_element(topology)
        self.endElement('grenml:Topology')


class InstitutionWriter(Writer):

    def write_element(self, institution: Institution):
        self.startElement('grenml:Institution', {
            'id': institution.id,
            'version': institution.version
        })
        self.element('grenml:name', institution.name)
        self.element('grenml:short-name', institution.short_name)
        for inst_type in institution.types:
            self.element('grenml:type', inst_type)
        LocationWriter(self.stream).write_element(institution)
        self.write_properties(institution.additional_properties)
        self.endElement('grenml:Institution')


class LinkWriter(Writer):

    def write_element(self, link: Link):
        self.startElement('grenml:Link', {
            'id': link.id,
            'version': link.version
        })
        self.element('grenml:name', link.name)
        self.element('grenml:short-name', link.short_name)
        for owner in link.owners:
            self.element('grenml:owner', owner.id)
        LifetimeWriter(self.stream).write_element(link)
        for name, values in link.additional_properties.items():
            for value in values:
                self.element('grenml:Property', value, {'name': name})
        for node in link.nodes:
            self.element('grenml:node', node.id)
        self.endElement('grenml:Link')


class NodeWriter(Writer):

    def write_element(self, node: Node):
        self.startElement('grenml:Node', {
            'id': node.id,
            'version': node.version
        })
        self.element('grenml:name', node.name)
        self.element('grenml:short-name', node.short_name)
        for owner in node.owners:
            self.element('grenml:owner', owner.id)
        LifetimeWriter(self.stream).write_element(node)
        LocationWriter(self.stream).write_element(node)
        self.write_properties(node.additional_properties)
        self.endElement('grenml:Node')


class LocationWriter(Writer):

    def write_element(self, element: GRENMLObject):
        # Only write the location if there is any tags to be written
        if getattr(element, 'longitude', None) \
           or getattr(element, 'latitude', None) \
           or getattr(element, 'altitude', None) \
           or getattr(element, 'ulocode', None) \
           or getattr(element, 'address', None):
            self.startElement('grenml:Location')
            self.element(
                'grenml:long', getattr(element, 'longitude', None)
            )
            self.element(
                'grenml:lat', getattr(element, 'latitude', None)
            )
            self.element(
                'grenml:alt', getattr(element, 'altitude', None)
            )
            self.element(
                'grenml:unlocode', getattr(element, 'unlocode', None)
            )
            for address in getattr(element, 'addresses', []):
                self.element(
                    'grenml:address', address
                )
            self.endElement('grenml:Location')


class LifetimeWriter(Writer):

    def write_element(self, element: GRENMLObject):
        if hasattr(element, 'lifetime_start'):
            self.startElement('grenml:Lifetime')
            self.element('nml:start', element.lifetime_start)
            self.element('nml:end', element.lifetime_end)
            self.endElement('grenml:Lifetime', )
