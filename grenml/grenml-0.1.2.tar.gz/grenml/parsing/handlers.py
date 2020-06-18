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

Synopsis: GRENML base content handlers for parsing SAX content
"""

import inspect
from grenml.parsing.exceptions import UnexpectedElementException
from grenml.parsing.exceptions import MissingAttributeException
from grenml import GRENMLManager


class ElementHandler:
    """
    Base element handler that allows for automatic traversal of the dom
    """

    # Name of the element
    element_name = None

    def __init__(self, parent, manager: GRENMLManager):
        self.parent_handler = parent
        self.manager = manager

    def startElement(self, name, attrs):
        """
        Called when an element matching the element name is encountered
        """
        pass

    def characters(self, characters):
        """
        Called when text content is encountered inside the element
        """
        pass

    def endElement(self, name):
        """
        Called when a closing element matching the element name is encountered
        """
        pass

    def getHandler(self, name):
        for i in self.__class__.__dict__.values():
            if inspect.isclass(i) and issubclass(i, ElementHandler):
                if i.element_name == name:
                    return i
        raise UnexpectedElementException(self.element_name, name)

    def getRequiredAttribute(self, attrs, name):
        """
        Returns the value of an attribute that is expected to exist
        raises an exception if it is not found
        """
        try:
            return attrs.get(name)
        except KeyError:
            raise MissingAttributeException(self.element_name, name)


class RecursiveElementHandler(ElementHandler):
    """
    An extention of the base element handler, allowing for an element
    to handle instances of itself
    """

    def getHandler(self, name):
        try:
            return super().getHandler(name)
        except UnexpectedElementException:
            if name == self.element_name:
                return self.__class__
            else:
                raise UnexpectedElementException(self.element_name, name)


class NMLElementHandler(RecursiveElementHandler):
    def getHandler(self, name):
        try:
            return super().getHandler(name)
        except UnexpectedElementException:
            if name == self.element_name:
                return self.__class__
            else:
                raise UnexpectedElementException(self.element_name, name)
