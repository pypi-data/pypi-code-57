import networkx as nx
import matplotlib.pyplot as plt

from copy import deepcopy


DEFAULT_IMAGE_NAME = "dependency_graph.png"


class GraphNotFullyExecutableError(Exception):
    pass


class GraphNotExecutableError(Exception):
    pass


class ExecutableDirectedMultiGraph(nx.MultiDiGraph):
    def __init__(self, *args, **kwargs):
        super(ExecutableDirectedMultiGraph, self).__init__(*args, **kwargs)

    @staticmethod
    def search_root_nodes(graph):
        return [n for n in graph.nodes if graph.in_degree(n) == 0]

    @staticmethod
    def get_execution_order(graph):
        execution_order = []
        cloned_graph = deepcopy(graph)
        while len(cloned_graph.nodes) > 0:
            roots = ExecutableDirectedMultiGraph.search_root_nodes(cloned_graph)
            execution_order += roots
            for root_node in roots:
                cloned_graph.remove_node(root_node)
        return execution_order

    @staticmethod
    def get_node_colors(graph):
        color_map = []
        for node in graph.nodes:
            f = graph.nodes[node].get("function")
            if f is not None and callable(f):
                color_map.append("green")
            else:
                color_map.append("red")

        return color_map

    def is_fully_executable(self):
        for node in self.nodes:
            function = self.nodes[node].get("function")
            if not callable(function):
                return False

        try:
            nx.find_cycle(self)
            print("Graph contains a cycle")
            return False
        except nx.NetworkXNoCycle:
            pass

        return True

    def execute(self):
        if not self.is_fully_executable():
            raise GraphNotFullyExecutableError

        execution_order = self.get_execution_order(self)

        for node in execution_order:
            function_arguments = self.nodes[node].get("function_arguments", [])
            function_context = {p: self.nodes[p].get("return_value") for p in self.predecessors(node)}
            self.nodes[node]["return_value"] = \
                self.nodes[node].get("function")(*function_arguments, context=function_context)

    def partial_execute(self):
        raise NotImplementedError

    def simulate_execute(self):
        if not self.is_fully_executable():
            raise GraphNotFullyExecutableError

        execution_order = self.get_execution_order(self)

        print("The node functions will be executed in the following order: \n")
        print("\n".join(execution_order))

        print("Simulating the function calls:")
        for node in execution_order:
            function_arguments = self.nodes[node].get("function_arguments", [])
            function_name = self.nodes[node].get("function").__name__

            message = f"Calling function {function_name} "
            if len(function_arguments) > 0:
                message += f"with arguments {', '.join(function_arguments)}"
            print(message)

    def display_graph(self):
        color_map = self.get_node_colors(self)
        nx.draw(self, with_labels=True, node_color=color_map)
        plt.show()

    def save_graph(self, name=DEFAULT_IMAGE_NAME):
        color_map = self.get_node_colors(self)
        nx.draw(self, with_labels=True, node_color=color_map)
        plt.savefig(name)

    def save_and_display_graph(self, name=DEFAULT_IMAGE_NAME):
        color_map = self.get_node_colors(self)
        nx.draw(self, with_labels=True, node_color=color_map)
        plt.savefig(name)
        plt.show()
