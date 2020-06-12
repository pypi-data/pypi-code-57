import re
import networkx as nx
import pydotplus
import warnings
import copy


def find_cluster_recursive(graph, cluster):
    """
    :param graph: a graph in which to search for cluster and look for subgraphs
    :param cluster: cluster name (str)
    :return: graph that is cluster
    """
    if cluster[:8] != "cluster_":
        cluster = "cluster_" + cluster
    if graph.obj_dict["name"] == cluster:
        return graph
    # repeat for every subgraph in graph (recursively)
    for subgraph in graph.get_subgraph_list():
        result = find_cluster_recursive(subgraph, cluster)
        if result:
            return result


def find_parent_recursive(graph, node):
    """
    :param graph: a graph in which to search for parent and look for subgraphs
    :param node: node name (str)
    :return: name of parent graph
    """
    if node in graph.obj_dict["nodes"].keys():
        return graph.obj_dict["name"].split("cluster_")[1]
    # repeat for every subgraph in graph (recursively)
    for subgraph in graph.get_subgraph_list():
        result = find_parent_recursive(subgraph, node)
        if result:
            return result


def filter_node_list(node_list):
    """
    Remove duplicated nodes and "graph" from list of node names

    :param node_list: list of node names (str)
    :return: set of node names, where "graph" is excluded
    """
    # TODO feels a bit over the top to put this in a function
    return set([node for node in node_list if node != "graph"])


def del_node_recursive(graph, node):
    # TODO: static method, move to helper module?
    """
    :param graph: a graph in which to delete nodes and look for subgraphs
    :param node: node name (str)
    """
    graph.del_node(node)
    for subgraph in graph.get_subgraph_list():
        del_node_recursive(subgraph, node)


def split_func_str(func_str):
    """
    :param func_str: e.g. "bacon__eggs"
    :return: ("bacon", "eggs")
    """
    # derive the number of functions in the func_str
    n_func = len([sub_func for sub_func in func_str.split("__") if sub_func != ""])
    # construct regex pattern based on number of functions
    # this ensures that we have enough regex capture groups
    # (regex's own repeat pattern functionality didn't work well in this respect)
    regex_pattern_partial = "(__.*[^_]__|.*[^_])"
    regex_pattern = "__".join([regex_pattern_partial] * n_func)
    # make sure output is tuple
    split_func = re.findall(regex_pattern, func_str)[0]
    if type(split_func) == str:
        split_func = tuple([split_func])
    return split_func


"""
VeazyHelper is built around two assumptions:
* A function name never contains '__' within the function name 
    (though at start/end is fine, like __init__)
* A function name never contains '___'

Our dependency pyan3 doesn't like relative imports
"""


class Veazy:
    def __init__(self, pyg, root_file):
        if root_file == "":
            raise Exception("Please provide a root file")
        try:
            self.top_node = re.sub(".py", "", root_file)
        except nx.exception.NodeNotFound:
            raise ValueError(
                "The supplied root file does not call any "
                "methods or functions in the supplied graph"
            )

        self.depth_of_nodes = {}
        self.node_list = []
        self.pyg = pyg
        # keep a copy that won't be mutated
        self.pyg_org = copy.deepcopy(pyg)
        self.script_node_list = []
        self.too_deep_nodes = []
        self.too_deep_edges = []

        self._fill_filter_node_lists()
        self._fill_depth_of_nodes()

    def _fill_filter_node_lists(self):
        """
        Fill and filter self.node_list and fill self.script_nodes
        """
        self.node_list = []
        self._fill_node_list(self.pyg)
        self.node_list = filter_node_list(self.node_list)
        # The first subgraph contains nodes that are scripts
        self.script_node_list = list(
            self.pyg.get_subgraph_list()[0].obj_dict["nodes"].keys()
        )
        self.script_node_list = filter_node_list(self.script_node_list)
        # remove top node from script nodes
        self.script_node_list = [i for i in self.script_node_list if i != self.top_node]

    def _fill_node_list(self, graph):
        """
        Fill self.node_list by finding all nodes in graph
        and recursively calling this function to all subgraphs in graph

        :param graph: pydot graph
        """
        self.node_list += list(graph.obj_dict["nodes"].keys())
        for subgraph in graph.get_subgraph_list():
            self._fill_node_list(subgraph)

    def _fill_depth_of_nodes(self):
        """
        Fill self.depth_of_nodes, calc shortest path from self.top_node to all nodes
        """
        self.depth_of_nodes = {}

        # utilize networkx to calculate depth
        nxg = nx.drawing.nx_pydot.from_pydot(self.pyg)

        # calculate depth of nodes, based on first node
        try:
            self.depth_of_nodes = dict(
                nx.single_source_shortest_path_length(nxg, self.top_node)
            )
        except nx.NodeNotFound as e:
            raise Exception(
            [
                e, 
                Exception(
                    "Your root file probably doesn't contain a function, "
                    "or doesn't call any of the other files"
                )
            ]
        )

        # There could be nodes that do not have a relation to the top node,
        # force fill these here
        missing_depths = {}
        for node in self.node_list:
            if node not in self.depth_of_nodes.keys():
                if node in self.script_node_list:
                    missing_depths[node] = 0
                else:
                    # TODO: does this work correctly, and do we want this `here`?
                    # if a node doesn't have a relation to the top node,
                    # and if it's not a script node, delete it
                    self._delete_node_edge([node])
        self.depth_of_nodes = {**self.depth_of_nodes, **missing_depths}

    def _find_edges(self, nodes_to_search):
        """
        :param nodes_to_search: list of node names (str)
        :return: list of edge tuples
        """
        return [
            edge
            # contrary to nodes, self.pyg contains all edges
            for edge in self.pyg.obj_dict["edges"].keys()
            if any(i in nodes_to_search for i in edge)
        ]

    def _delete_node_edge(self, nodes):
        """
        Delete nodes and their related edges from self.pyg
        :param nodes: list of node names (str)
        """
        for node in nodes:
            del_node_recursive(self.pyg, node)
        for edge in self._find_edges(nodes):
            self.pyg.del_edge(edge)
        self._fill_filter_node_lists()

    def _fill_too_deep(self, max_depth):
        """
        Fill self.nodes_to_deep and self.edges_to_deep with too deep nodes/edges
        :param max_depth: int to identify which nodes/edges are to deep
        """
        self.too_deep_nodes = []
        self.too_deep_edges = []

        self.too_deep_nodes = [
            node for node, depth in self.depth_of_nodes.items() if depth > max_depth
        ]
        self.too_deep_edges = self._find_edges(self.too_deep_nodes)

    def _get_summarized_name(self, node, max_depth):
        # TODO: this might need an escape where summarized_node will default to ""
        """
        Find not-to-deep parent of node.
        This level will be returned as summarizing node.
        :param node: node name (str)
        :return: summarizing name for node
        """
        summarized_node = node
        try:
            # first check if there is a parent node that we can use as summarizing node
            while self.depth_of_nodes[summarized_node] > max_depth:
                summarized_node = find_parent_recursive(self.pyg_org, summarized_node)
        except KeyError:
            # if we cannot find such a node, derive summarizing node based on node name
            summarized_node = "__".join(
                split_func_str(node)[
                    : (
                        len(split_func_str(node))
                        - (self.depth_of_nodes[node] - max_depth)
                    )
                ]
            )
        if summarized_node != node:
            summarized_node = "SUMMARIZED_FROM_" + summarized_node
        return summarized_node

    def _add_summarizing(self, max_depth):
        """
        Based on max_depth, add summarizing nodes to graph
        :param max_depth: int
        """
        # From the deleted nodes, find level that is not to deep.
        # This level will be re-added as summarizing node.
        summarizing_nodes = set(
            [self._get_summarized_name(node, max_depth) for node in self.too_deep_nodes]
        )
        summarizing_edges = []
        for edge in self.too_deep_edges:
            summarizing_edges.append(
                (
                    self._get_summarized_name(edge[0], max_depth),
                    self._get_summarized_name(edge[1], max_depth),
                )
            )
        # TODO: is this working as expected?
        # keep edges of which both nodes are in summarizing_nodes or in self.node_list
        summarizing_edges = [
            edge
            for edge in summarizing_edges
            if all([i in summarizing_nodes or i in self.node_list for i in edge])
        ]
        for node in summarizing_nodes:
            # TODO: do we still have node == "" with updated _get_summarized_name()?
            if node != "":
                graph_to_add_to = find_cluster_recursive(
                    self.pyg, node.split("SUMMARIZED_FROM_")[1]
                )
                # TODO: can `if` below be incorporated into recursive function?
                if not graph_to_add_to:
                    graph_to_add_to = self.pyg
                graph_to_add_to.add_node(pydotplus.graphviz.Node(name=node))
        for edge in set(summarizing_edges):
            if "" not in edge:
                self.pyg.add_edge(pydotplus.graphviz.Edge(src=edge[0], dst=edge[1]))
        # TODO: There are quite a few functions where this is called at the end.
        #  Rewrite to decorator?
        self._fill_filter_node_lists()

    def _add_final_summarizing(self):
        """
        After the first step of summarization, collapse all summarized nodes
        that are still to deep to "..."
        """
        # Add the ... node, but only when necessary
        if len(self.too_deep_edges) > 0:
            self.pyg.get_subgraph_list()[0].add_node(
                pydotplus.graphviz.Node(name="...")
            )
        # summarize all relevant edges
        summarizing_edges = []
        for edge in self.too_deep_edges:
            e0 = edge[0] if edge[0] not in self.too_deep_nodes else "..."
            e1 = edge[1] if edge[1] not in self.too_deep_nodes else "..."
            summarizing_edges.append((e0, e1))
        # remove edges from ... to ...
        summarizing_edges = set(
            [
                edge
                for edge in summarizing_edges
                if not all([node == "..." for node in edge])
            ]
        )
        for edge in summarizing_edges:
            self.pyg.add_edge(pydotplus.graphviz.Edge(src=edge[0], dst=edge[1]))
        self._fill_filter_node_lists()

    def _find_max_depth_from_max_nodes(self, max_nodes):
        """
        Find a depth that would depict approximately n nodes
        :param max_nodes: n nodes for which to find max_depth (int)
        :return: max_depth (int)
        """

        def n_nodes_if_depth(depth):
            """
            :param depth: int
            :return: number of nodes that would be depicted based on this depth
            """
            return sum([i < depth for i in self.depth_of_nodes.values() if i != 0])

        max_depth = 1
        while n_nodes_if_depth(max_depth) < max_nodes:
            max_depth += 1
            if max_depth == (max(self.depth_of_nodes.values()) + 1):
                break
        # inspect if one depth lower would be closer to max_nodes
        if abs(n_nodes_if_depth(max_depth - 1) - max_nodes) < abs(
            n_nodes_if_depth(max_depth) - max_nodes
        ):
            max_depth -= 1
        return max_depth

    def find_auto_depth(self):
        """
        User callable method that returns the depth corresponding to approx 30 nodes
        :return: max_depth
        """
        return self._find_max_depth_from_max_nodes(30)

    def prune_depth(self, max_depth):
        """
        User callable method that returns a pruned graph based on max_depth
        :param max_depth: int
        :return: pruned graph
        """
        if max_depth < 1:
            warnings.warn(
                f"The max_depth that was passed({max_depth}) will be ignored, "
                "and set to the minimum value of 1"
            )
        max_depth = max(1, max_depth - 1)
        self._fill_depth_of_nodes()
        self._fill_too_deep(max_depth)
        self._delete_node_edge(self.too_deep_nodes)
        # remove script nodes (apart from top_node)
        self._delete_node_edge(self.script_node_list)
        self._add_summarizing(max_depth)
        # after first run of summarizing nodes, there can be summarizing nodes
        # that are itself to deep. We will summarize these further, to ...
        self._fill_depth_of_nodes()
        self._fill_too_deep(max_depth + 1)
        self._delete_node_edge(self.too_deep_nodes)
        # remove top script node
        self._delete_node_edge([self.top_node])
        self._add_final_summarizing()
        return self.pyg

    def prune_width(self, max_nodes):
        """
        User callable method that returns a pruned graph based on max_nodes
        :param max_nodes: int
        :return: pruned graph
        """
        max_depth = self._find_max_depth_from_max_nodes(max_nodes)
        return self.prune_depth(max_depth)

    def prune_auto(self):
        """
        User callable method that returns a pruned graph with approximately 30 nodes
        :return: pruned graph
        """
        max_depth = self.find_auto_depth()
        return self.prune_depth(max_depth)
