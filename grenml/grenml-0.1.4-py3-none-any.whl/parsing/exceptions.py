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

Synopsis: Collection of exceptions that may be thrown by the GRENML handlers
"""


class GRENMLException(Exception):
    """
    Base exception for GRENML parsing
    """
    pass


class MissingAttributeException(GRENMLException):
    """
    A required attribute could not be found when parsing an element
    """

    def __init__(self, element_name, expected_attribute):
        self.element_name = element_name
        self.expected_attribute = expected_attribute

    def __str__(self):
        return ("Missing attribute {} while parsing <{}>").format(
            self.expected_attribute,
            self.element_name,
        )


class UnexpectedElementException(GRENMLException):
    """
    An element was encountered during parsing that was not expected
    """

    def __init__(self, element_name, unexpected_element):
        self.element_name = element_name
        self.unexpected_element = unexpected_element

    def __str__(self):
        return "Got unexpected <{}> while parsing <{}>".format(
            self.unexpected_element,
            self.element_name,
        )
