from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
class JanusGraphHelper:
    def __init(self,host,port,scheme):
        g = Graph()
        url = "ws://{0}:{1}/{3}".format(host,port,scheme)
        graph = g.traversal().withRemote(DriverRemoteConnection(url, 'g'))
        self.graph = graph
    def add_vertex(self, label, properties=None):
        """
        add vertex
        :param graph: graph, type: GraphTraversalSource
        :param label: label, type: str
        :param properties: property dict, like {'p1': 'value1', 'p2': 'value2'}
        :return: vertex, Vertex(id, label)
        """
        vert = self.graph.addV(label)
        if properties:
            for key in properties.keys():
                vert.property(key, properties.get(key))
        return vert.next()

    def add_edge(self, label, v_from, v_to, properties=None):
        """
        add edge
        :param graph: graph, type: GraphTraversalSource
        :param label: label, type: str
        :param v_from: long vertex id or Vertex(id, label) of from
        :param v_to: long vertex id or Vertex(id, label) of to
        :param properties: property dict, like {'p1': 'value1', 'p2': 'value2'}
        :return: None
        """
        if isinstance(v_from, int):
            v_from = self.graph.V().hasId(v_from).next()
        if isinstance(v_to, int):
            v_to = self.graph.V().hasId(v_to).next()
        edge = self.graph.V(v_from).addE(label).to(v_to)
        if properties:
            for key in properties.keys():
                edge.property(key, properties.get(key))
        edge.next()

    def drop_vertex(self, v_id=None, label=None, properties=None):
        """
        drop all vertex or specific vertex
        :param graph: graph, type: GraphTraversalSource
        :param v_id: long vertex id or Vertex(id, label)
        :param label: label, type: str
        :param properties: property list, like ['p1', 'p2', {'p3': 'value'}]
        :return: None
        """
        if isinstance(v_id, int):
            v_id = self.graph.V().hasId(v_id).next()
        travel = self.graph.V(v_id) if v_id else self.graph.V()
        if label:
            travel = travel.hasLabel(label)
        if properties:
            for p in properties:
                if isinstance(p, dict):
                    key = list(p.keys())[0]
                    travel = travel.has(key, p.get(key))
                else:
                    travel = travel.has(p)
        travel.drop().iterate()

    def drop_edge(self, e_id=None, label=None, properties=None):
        """
        drop all edges or specific edge
        :param graph: graph, type: GraphTraversalSource
        :param e_id: edge id, type str
        :param label: label, type: str
        :param properties: property list, like ['p1', 'p2', {'p3': 'value'}]
        :return: None
        """
        travel = self.graph.E(e_id) if e_id else self.graph.E()
        if label:
            travel = travel.hasLabel(label)
        if properties:
            for p in properties:
                if isinstance(p, dict):
                    key = list(p.keys())[0]
                    travel = travel.has(key, p.get(key))
                else:
                    travel = travel.has(p)
        travel.drop().iterate()

    def query_vertex(self, v_id=None, label=None, properties=None):
        """
        query graph vertex (value) list
        :param graph: graph, type: GraphTraversalSource
        :param v_id: long vertex id or Vertex(id, label)
        :param label: label, type: str
        :param properties: property list, like ['p1', 'p2', {'p3': 'value'}]
        :return: vertex list or vertex value list
        """
        if isinstance(v_id, int):
            v_id = self.graph.V().hasId(v_id).next()
        travel = self.graph.V(v_id) if v_id else self.graph.V()
        if label:
            travel = travel.hasLabel(label)
        if properties:
            for p in properties:
                if isinstance(p, dict):
                    key = list(p.keys())[0]
                    travel = travel.has(key, p.get(key))
                else:
                    travel = travel.has(p)
        # return travel.valueMap().toList()
        return travel.toList()

    def query_edge(self, e_id=None, label=None, properties=None):
        """
        query graph edge value list
        :param graph: graph, type: GraphTraversalSource
        :param e_id: edge id, type str
        :param label: label, type: str
        :param properties: property list, like ['p1', 'p2', {'p3': 'value'}]
        :return: valueMap list
        """
        travel = self.graph.E(e_id) if e_id else self.graph.E()
        if label:
            travel = travel.hasLabel(label)
        if properties:
            for p in properties:
                if isinstance(p, dict):
                    key = list(p.keys())[0]
                    travel = travel.has(key, p.get(key))
                else:
                    travel = travel.has(p)
        return travel.valueMap().toList()

    def query_edges_of_vertex(self, v_id):
        """
        query all edges of vertex
        :param graph: graph, type: GraphTraversalSource
        :param v_id: v_id: long vertex id or Vertex(id, label)
        :return: edge list
        """
        if isinstance(v_id, int):
            v_id = self.graph.V().hasId(v_id).next()
        result = []
        in_edges = self.graph.V(v_id).inE().toList()
        out_edges = self.graph.V(v_id).outE().toList()
        result.extend(in_edges)
        result.extend(out_edges)
        return result

    def query_near_vertex(self, v_id):
        """
        query near vertices of vertex
        :param graph: graph, type: GraphTraversalSource
        :param v_id: v_id: long vertex id or Vertex(id, label)
        :return: vertex list
        """
        if isinstance(v_id, int):
            v_id = self.graph.V().hasId(v_id).next()
        result = []
        out_v = self.graph.V(v_id).out().toList()
        in_v = self.graph.V(v_id).in_().toList()
        result.extend(out_v)
        result.extend(in_v)
        return result

    def get_edge_id(self,edge):
        """
        get edge id
        :param edge: Egde(id, label, outV, inV)
        :return: edge id, type str
        """
        return edge.id.get('@value').get('relationId')

    def vertex_to_dict(self, vertex):
        """
        transfer Vertex's info to dict
        :param graph: graph, type: GraphTraversalSource
        :param vertex: vertex, Vertex(id, label)
        :return: vertex info dict
        """
        properties = self.graph.V(vertex).valueMap().toList()[0]
        for key in properties.keys():
            properties[key] = properties.get(key)[0]
        return {
            'id': vertex.id,
            'label': vertex.label,
            'properties': properties
        }

    def edge_to_dict(self, edge):
        """
        transfer Edge's info to dict
        :param graph: graph, type: GraphTraversalSource
        :param edge: edge, Edge(id, label, outV, inV)
        :return: edge info dict
        """
        e_id = get_edge_id(edge)
        properties = self.graph.E(e_id).valueMap().toList()[0]
        return {
            'id': e_id,
            'label': edge.label,
            'properties': properties
        }

    def judge_vertex_in_graph(self, vertex_dict):
        """
        judge a vertex whether in graph
        :param graph: graph, type: GraphTraversalSource
        :param vertex_dict: vertex dict, like {'label': 'value1', 'properties': {'p1': 'v1', ...}}
        :return: None or Vertex(id,label)
        """
        label = vertex_dict.get('label')
        properties = vertex_dict.get('properties')
        travel = self.graph.V()
        if label:
            travel = travel.hasLabel(label)
        if properties:
            for k in properties.keys():
                travel = travel.has(k, properties.get(k))
        if travel.hasNext():
            return travel.next()
        return None

    def get_sub_graph(self, vertices=None, edges=None, vertex_properties=None):
        """
        get sub graph
        :param graph: graph, type: GraphTraversalSource
        :param vertices: hasLabel('label').has('property').has('age', gt(20))
        :param edges: hasLabel('label').has('property')
        :param vertex_properties:
        :return: sub_graph, type: GraphTraversalSource
        """
        strategy = SubgraphStrategy(vertices=vertices, edges=edges, vertex_properties=vertex_properties)
        return self.graph.withStrategies(strategy)
