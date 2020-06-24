from functools import cached_property
from typing import Dict, List

from .node import Node


class Tree(object):
    CONST_CACHED_PROPERTIES = ["leaf_names"]

    def __init__(self, root=None):
        self.name_key_map: Dict[str, str] = {}
        self.key_node_map: Dict[str, Node] = {}
        self.root: Node = root

    def to_dict(self) -> dict:
        response = self.root.to_dict()
        response["children"] = [child.to_dict() for child in self.root.children]
        return response

    @property
    def root(self):
        return self.__root

    @root.setter
    def root(self, tree_input):
        if isinstance(tree_input, Node):
            # don't use -> only used for testing
            self.__root = tree_input
        elif isinstance(tree_input, dict):
            self.__root = self.from_dict(tree_input)
        else:
            raise TypeError(
                "Expected: tree_input <class 'Node | dict'>, Received: {0}".format(
                    type(tree_input)
                )
            )

    @cached_property
    def leaf_names(self) -> List[str]:
        leaf_names = []

        for node in self.key_node_map.values():
            if len(node.children) == 0:
                leaf_names.append(node.name)

        return leaf_names

    def node(self, name: str) -> Node:
        """Retruns a Node with matching name if it exists in the Tree.

        Parameters:
        - name: str - the name of the Node

        Returns:
        - node: Node - the Node in the Tree with a matching name

        Raises:
        - KeyError: if name does not exist
        """
        key = self.node_key(name)
        return self.__node_by_key(key)

    def node_key(self, name: str) -> str:
        return self.name_key_map[name]

    def __node_by_key(self, key: str) -> Node:
        return self.key_node_map[key]

    def __invalidate_cache(self):
        """Invalidates all cache entries of the class by
        clearing the lru_cache for the function calls with arguments
        and by clearing all cached_properties.
        """
        # clear all cached properties
        for prop in self.CONST_CACHED_PROPERTIES:
            self.__invalidate_cached_property(prop)

    def __invalidate_cached_property(self, name: str):
        """Deletes the dict entry of a cached property.
        """
        if name in self.__dict__:
            del self.__dict__[name]

    def from_dict(self, tree_input: dict) -> Node:
        """Creates a Tree from a dict of nodes.

        Parameters:
        - root: dict - the input JSON as a dictionary
        - LOG: bool - flag to decide if the creation of the nodes shall be logged

        Returns:
        - root: Node - the root Node of the tree including all children
        """
        # invalidate cache entries (since Tree changes)
        self.__invalidate_cache()

        # create the Tree recursively from the JSON input
        return self.__rec_create_nodes_from_dict("0", tree_input["tree_input"])

    def __rec_create_nodes_from_dict(self, index: str, tree_input: dict) -> Node:
        # base case: node has no children -> it is a leaf
        if len(tree_input["children"]) == 0:
            # create a leaf node and assign the value
            leaf = Node(
                key=index,
                name=tree_input["name"],
                description=tree_input["description"],
                value=tree_input["value"],
            )

            # create mapping name -> key
            self.name_key_map[tree_input["name"]] = index

            # create mapping key -> node
            self.key_node_map[index] = leaf
            return leaf

        # recursion: node has children -> it is a parent
        else:
            children = []
            parent_index = index

            # create parent without children
            parent = Node(
                key=parent_index,
                name=tree_input["name"],
                description=tree_input["description"],
            )

            # create mapping name -> key
            self.name_key_map[tree_input["name"]] = index

            for index_, child_json in enumerate(tree_input["children"]):
                child_index = parent_index + str(index_)

                # recursively call each child and see if it has children
                child = self.__rec_create_nodes_from_dict(child_index, child_json)
                children.append(child)

            parent.children = children

            # create mapping key -> node
            self.key_node_map[parent.key] = parent
            return parent
