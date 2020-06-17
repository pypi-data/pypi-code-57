import pydot


class Visualization(object):
    def __init__(self, config):
        self.config = config
        # http://www.graphviz.org/Documentation.php
        self.graph = pydot.Dot(graph_type='digraph')
        self.nodes_list = []
        self.nodes = [{
            "name": "",
            "node_object": object,
            "edge_to_name": "",
            "edge_to_object": object,
            "edge_label": "",
        }]
        self.colors = ["red", "green", "blue", "pink", "red", "green", "blue", "pink", "red", "green", "blue", "pink"]

    def create_nodes(self):
        for i, node in enumerate(self.nodes):
            new_node = pydot.Node(node["name"], style="filled", fillcolor=self.colors[i])
            self.nodes_list.append(new_node)
            node["node_object"] = new_node
            self.graph.add_node(new_node)

        for i, node in enumerate(self.nodes):
            edge_to_object = [next_node for next_node in self.nodes_list if next_node.get_name() == node["edge_to_name"]]  # pydot.Node(node["name"], style="filled", fillcolor=self.colors[i])
            if edge_to_object:
                edge_to_object = edge_to_object.pop()
                node["edge_to_object"] = edge_to_object
                self.graph.add_edge(pydot.Edge(node["node_object"], edge_to_object, label=node.get("edge_label", ""), labelfontcolor="#009933", fontsize="10.0", color="blue"))

    def print_g(self):
        self.graph.write_png('example.png')
