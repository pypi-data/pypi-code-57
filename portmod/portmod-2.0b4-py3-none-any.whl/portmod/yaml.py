# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""PyYAML wrapper to avoid breaking compatibility with older versions of PyYAML"""

import yaml

try:
    from yaml import CFullLoader as Loader  # type: ignore
except ImportError:
    try:
        from yaml import FullLoader as Loader
    except ImportError:
        from yaml import Loader as Loader


class Person(yaml.YAMLObject):
    yaml_tag = "!person"
    yaml_loader = Loader

    def __init__(self, name="", email="", desc=""):
        self.update(name, email, desc)

        if not name and not email:
            raise Exception("Cannot create empty Person")

    def update(self, name, email, desc):
        self.name = name
        self.email = email
        self.desc = desc

    def __str__(self):
        if self.name and not self.email:
            return self.name
        elif not self.name and self.email:
            return self.email
        elif self.name and self.email:
            return "{} <{}>".format(self.name, self.email)
        else:
            raise Exception("Trying to transform an empty Person to a string")

    def __repr__(self):
        return "{}(name={}, email={}, desc={})".format(
            self.__class__.__name__, self.name, self.email, self.desc
        )

    @classmethod
    def from_yaml(cls, loader, node):
        if isinstance(node, yaml.ScalarNode):
            return Person(node.value)
        else:
            node_map = loader.construct_mapping(node, deep=True)
            return Person(**node_map)


class Group(yaml.YAMLObject):
    yaml_tag = "!group"
    yaml_loader = Loader

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "%s(name=%r)" % (self.__class__.__name__, self.name)

    @classmethod
    def from_yaml(cls, loader, node):
        if isinstance(node, yaml.ScalarNode):
            return Group(node.value)
        else:
            node_map = loader.construct_mapping(node, deep=True)
            return Group(**node_map)


def yaml_load(file):
    """
    Loads yaml file

    Attempt to use the safer FullLoader, but fall back to unsafe load
    to avoid breaking compatibility
    """
    return yaml.load(file, Loader=Loader)
