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

Synopsis: The custom exceptions that can be raised by GRENML
"""


class AttributeNameError(AttributeError):
    """
    Attribute `name` must be a human readable string name.
    """
    pass


class AttributeIdError(AttributeError):
    """
    Attribute `identifier` must be a persistent globally unique URI.
    """
    pass


class AttributeOwnerError(AttributeError):
    """
    Attribute 'owner' must be an Institution Object
    """
    pass


class AttributeNodeError(AttributeError):
    """
    The attribute nodes must contain only Node objects and
    """
    pass


class AttributeLongitudeError(AttributeError):
    """
    Attribute Longitude was given an invalid coordinate. (gt 180 or lt -180)
    """
    pass


class AttributeLatitudeError(AttributeError):
    """
    Attribute Latitude was given an invalid coordinate. (gt 90 or lt -90)
    """
    pass


class ObjectNotFoundError(Exception):
    """
    Unable to locate object in a single item search
    """
    pass


class InstitutionNotFoundError(ObjectNotFoundError):
    """
    Unable to find an institution when searching for a single institution
    """
    pass


class NodeNotFoundError(ObjectNotFoundError):
    """
    Unable to find a node that meets search parameters
    """
    pass


class LinkNotFoundError(ObjectNotFoundError):
    """
    Unable to find a link that meets search parameters
    """
    pass


class TopologyNotFoundError(ObjectNotFoundError):
    """
    Unable to find the selected Topology
    """
    pass


class MultipleReturnedError(Exception):
    """
    A get single returned multiple values
    """
    pass
