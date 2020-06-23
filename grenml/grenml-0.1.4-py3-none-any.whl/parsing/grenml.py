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

Synopsis: Handlers for GRENML SAX events
"""

import xml.sax
from grenml.parsing.handlers import RecursiveElementHandler
from grenml.parsing.handlers import ElementHandler
from grenml.parsing.handlers import NMLElementHandler
from grenml.parsing.exceptions import GRENMLException
from grenml import GRENMLManager
from grenml.models import Institution, Node, Link, add_to_list


class GRENMLHandler(xml.sax.ContentHandler, ElementHandler):
    """
    Main handler for traversing the document and calling the
    appropriate handlers
    """

    def __init__(self):
        self.handler = self
        self.manager = GRENMLManager()
        self.character_cache = ''
        super().__init__()

    def startElement(self, name, attrs):
        try:
            self.handler = self.handler.getHandler(name)(
                self.handler,
                self.handler.manager
            )
            self.character_cache = ''
            self.handler.startElement(name, attrs)
        except GRENMLException as err:
            # Raise a SAX exception, since it handles the line/column number
            raise xml.sax.SAXParseException(str(err), None, self._locator)

    def characters(self, content):
        self.character_cache += content

    def endElement(self, name):
        self.handler.characters(self.character_cache)
        self.handler.endElement(name)
        self.character_cache = ''
        # If the current tag is ended, revert to the previous handler
        if name == self.handler.element_name:
            # If the handler is going to return back to this handler,
            # the final manager is the one in the grenml handler
            if self.handler.parent_handler == self:
                self.manager = self.handler.manager
            self.handler = self.handler.parent_handler

    class TopologyHandler(RecursiveElementHandler):

        element_name = "grenml:Topology"
        # TODO shouldn't need this, but currently the manager doesn't
        # allow you to set an owner before it exists
        owner_name = None

        def startElement(self, name, attrs):
            self.manager = GRENMLManager()
            self.manager.topology.id = self.getRequiredAttribute(attrs, 'id')
            self.manager.topology.version = attrs.get('version')

        def endElement(self, name):
            # If the parent handler is a topology, add itself to the parent
            # topology

            if isinstance(self.parent_handler, self.__class__):
                self.parent_handler.manager.topology.add_topology(
                    self.manager.topology
                )

        class NameHandler(ElementHandler):

            element_name = "grenml:name"

            def characters(self, content):
                self.manager.topology.name = content

        class OwnerHandler(ElementHandler):

            element_name = "grenml:owner"

            def characters(self, content):
                self.manager.set_primary_owner(content)
                pass

        class PropertyHandler(ElementHandler):

            element_name = "grenml:Property"

            # Name of the property being set
            name = None

            def startElement(self, name, attrs):
                self.name = self.getRequiredAttribute(attrs, 'name')

            def characters(self, content):
                self.manager.topology.add_property(self.name, content)

        class InstitutionHander(ElementHandler):

            element_name = "grenml:Institution"

            institution = None

            def startElement(self, name, attrs):
                self.institution = Institution(
                    id=self.getRequiredAttribute(attrs, 'id'),
                    version=attrs.get('version')
                )

            def endElement(self, name):
                # Quick fix. If an institution id is already in the manager, ignore it.
                if self.institution.id in self.manager.topology.institutions:
                    return
                self.manager.add_institution(self.institution)

            class NameHandler(ElementHandler):

                element_name = "grenml:name"

                def characters(self, content):
                    self.parent_handler.institution.name = content

            class ShortNameHandler(ElementHandler):

                element_name = "grenml:short-name"

                def characters(self, content):
                    self.parent_handler.institution.short_name = content

            class TypeHandler(ElementHandler):

                element_name = "grenml:type"

                def characters(self, content):
                    self.parent_handler.institution.type = add_to_list(
                        self.parent_handler.institution.type, content
                    )

            class LocationHandler(ElementHandler):

                def startElement(self, name, attrs):
                    self.parent_element = self.parent_handler.institution

                element_name = "grenml:Location"

                class LongHandler(ElementHandler):

                    element_name = "grenml:long"

                    def characters(self, content):
                        self.parent_handler.parent_element.longitude = float(content)

                class LatHandler(ElementHandler):

                    element_name = "grenml:lat"

                    def characters(self, content):
                        self.parent_handler.parent_element.latitude = float(content)
                    
                class AltitudeHandler(ElementHandler):

                    element_name = "grenml:alt"

                    def characters(self, content):
                        self.parent_handler.parent_element.altitude = float(content)

                class UnlocodeHandler(ElementHandler):

                    element_name = "grenml:unlocode"

                    def characters(self, content):
                        self.parent_handler.parent_element.unlocode = content

                class AddressHandler(ElementHandler):

                    element_name = "grenml:address"

                    def characters(self, content):
                        self.parent_handler.parent_element.address = content

            class PropertyHandler(ElementHandler):

                element_name = "grenml:Property"

                # Name of the property being set
                name = None

                def startElement(self, name, attrs):
                    self.name = self.getRequiredAttribute(attrs, 'name')

                def characters(self, content):
                    self.parent_handler.institution.add_property(self.name, content)

        class LinkHandler(ElementHandler):

            element_name = "grenml:Link"

            link = None

            def startElement(self, name, attrs):
                self.link = Link(
                    id=self.getRequiredAttribute(attrs, 'id'),
                    version=attrs.get('version')
                )

            def endElement(self, name):
                self.manager.add_link(self.link)

            class NameHandler(ElementHandler):

                element_name = "grenml:name"

                def characters(self, content):
                    setattr(self.parent_handler.link, 'name', content)

            class ShortNameHandler(ElementHandler):

                element_name = "grenml:short-name"

                def characters(self, content):
                    self.parent_handler.link.short_name = content

            class OwnerHandler(ElementHandler):

                element_name = "grenml:owner"

                def characters(self, content):
                    self.parent_handler.link.owners.add(content)

            class LifetimeHandler(ElementHandler):

                element_name = "grenml:Lifetime"

                class StartHandler(ElementHandler):

                    element_name = "nml:start"

                    def characters(self, content):
                        self.parent_handler.parent_handler.link.lifetime_start = content

                class EndHandler(ElementHandler):

                    element_name = "nml:end"

                    def characters(self, content):
                        self.parent_handler.parent_handler.link.lifetime_end = content

            class PropertyHandler(ElementHandler):

                element_name = "grenml:Property"

                # Name of the property being set
                name = None

                def startElement(self, name, attrs):
                    self.name = self.getRequiredAttribute(attrs, 'name')

                def characters(self, content):
                    self.parent_handler.link.add_property(self.name, content)

            class NodeHandler(ElementHandler):

                element_name = "grenml:node"

                def characters(self, content):
                    self.parent_handler.link.nodes.add(content)

        class NodeHandler(ElementHandler):

            element_name = "grenml:Node"

            node = None

            def startElement(self, name, attrs):
                self.node = Node(
                    id=self.getRequiredAttribute(attrs, 'id'),
                    version=attrs.get('version')
                )

            def endElement(self, name):
                self.manager.add_node(self.node)

            class NameHandler(ElementHandler):

                element_name = "grenml:name"

                def characters(self, content):
                    self.parent_handler.node.name = content

            class ShortNameHandler(ElementHandler):

                element_name = "grenml:short-name"

                def characters(self, content):
                    self.parent_handler.node.short_name = content

            class OwnerHandler(ElementHandler):

                element_name = "grenml:owner"

                def characters(self, content):
                    self.parent_handler.node.owners.add(content)

            class LifetimeHandler(ElementHandler):

                element_name = "grenml:Lifetime"

                class StartHandler(ElementHandler):

                    element_name = "nml:start"

                    def characters(self, content):
                        self.parent_handler.parent_handler.node.lifetime_start = content

                class EndHandler(ElementHandler):

                    element_name = "nml:end"

                    def characters(self, content):
                        self.parent_handler.parent_handler.node.lifetime_end = content

            class LocationHandler(ElementHandler):

                def startElement(self, name, attrs):
                    self.parent_element = self.parent_handler.node

                element_name = "grenml:Location"

                class LongHandler(ElementHandler):

                    element_name = "grenml:long"

                    def characters(self, content):
                        self.parent_handler.parent_element.longitude = float(content)

                class LatHandler(ElementHandler):

                    element_name = "grenml:lat"

                    def characters(self, content):
                        self.parent_handler.parent_element.latitude = float(content)
                    
                class AltitudeHandler(ElementHandler):

                    element_name = "grenml:alt"

                    def characters(self, content):
                        self.parent_handler.parent_element.altitude = float(content)

                class UnlocodeHandler(ElementHandler):

                    element_name = "grenml:unlocode"

                    def characters(self, content):
                        self.parent_handler.parent_element.unlocode = content

                class AddressHandler(ElementHandler):

                    element_name = "grenml:address"

                    def characters(self, content):
                        self.parent_handler.parent_element.add_address(content)

            class PropertyHandler(ElementHandler):

                element_name = "grenml:Property"

                # Name of the property being set
                name = None

                def startElement(self, name, attrs):
                    self.name = self.getRequiredAttribute(attrs, 'name')

                def characters(self, content):
                    self.parent_handler.node.add_property(self.name, content)

        class NMLTopologyHandler(NMLElementHandler):

            element_name = "nml:Topology"

            # We can not yet parse NML, but this can be used later
            pass
