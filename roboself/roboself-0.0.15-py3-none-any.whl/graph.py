import logging

from roboself.client import Client

log = logging.getLogger(__name__)


def _props_to_dict(props):
    """Helper for converting the node properties to a dict"""
    d = {}
    for k, v in props.items():
        # For node instances we just add references
        if isinstance(v, Node):
            d[k] = {"_ref": v.id}
        else:
            d[k] = v
    return d


class Node:
    """Node instance"""

    def __init__(self, graph, d):
        """Initialization using a dict from the API"""
        self.graph = graph

        if "_id" in d:
            self.id = d["_id"]
            self.has_data = True
            self.props = {}

            for k, v in d.items():
                if k[0] == "_":
                    continue

                # Check if we're dealing with a reference to another node
                if isinstance(v, dict) and (v.get("_id") is not None or v.get("_ref") is not None):
                    self.props[k] = Node(self.graph, v)
                else:
                    self.props[k] = v

        elif "_ref" in d:
            # for this type of nodes we'll fetch it on the fly if needed
            self.id = d["_ref"]
            self.has_data = False
            self.props = {}
        else:
            raise Exception("Invalid node format")

    def update(self, props):
        # to the update locally
        self.props.update(props)

        self.graph.client.request("/graph/node_update", {
            "node_id": self.id,
            "props": _props_to_dict(props)
        })

    def __getitem__(self, item):
        """Returns a property of a node"""
        return self.props.get(item)

    def __setitem__(self, key, value):
        """Updates the property of a node"""
        self.props[key] = value
        self.update({
            key: value
        })


class Graph:
    """Graph implementation on top of a RPC Client"""
    def __init__(self, client: Client):
        self.client = client

    def get_or_create(self, type_name, props):
        node_d = self.client.request("/graph/get_or_create", {
            "type_name": type_name,
            "props": _props_to_dict(props)
        })

        return Node(self, node_d)

    def get_nodes_by_type_and_props(self, type_name, props):
        node_ds = self.client.request("/graph/get_nodes_by_type_and_props", {
            "type_name": type_name,
            "props": _props_to_dict(props)
        })

        return [Node(self, node_d) for node_d in node_ds]
