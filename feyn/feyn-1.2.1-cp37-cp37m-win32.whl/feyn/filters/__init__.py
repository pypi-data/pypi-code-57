"""
A collection of filters to use with QGraphs.

A QGraph is a partially ordered infinite list of graphs with some constraints on the actual structure of the graphs.

One way to tune these constraints is to filter the QGraph with one or more filters from this package.

# Consider only graphs that are two deep and involve the "x" register.
> qgraph = qgraph.filter(feyn.filters.Depth(2))
> qgraph = qgraph.filter(feyn.filters.Contains("x"))
> qgraph.fit(data)

Notice that QGraph filters can be chained, and will be and'ed together.

This module has a useful collection of filters. It's also possible to define custom filters by deriving from the QGraphFilter baseclass
"""


from typing import List
from feyn import Graph

class QGraphFilter:
    """
    The abstract base class for QGraph Filters
    """
    def key(self) -> str:
        """
        Return a unique key for this filter. A QGraph can only have one filter with a given key, so filters can be made mutually exlusive using this method.

        When defining a filter that derives from this class, be sure to override this method and return a custom key.
        """
        return "basefilter"

    def __call__(self, graphs:List[Graph]) -> List[Graph]:
        """
        Perform the actual filtering. A derived class should implement this to return a filtered list or collection of graphs
        """
        return []

    def __repr__(self):
        return "abstact basefilter"

class Depth(QGraphFilter):
    """
    Use this class obtain a QGraph that only contain graphs of a certain depth.
    
    # Consider only graphs with depth 2
    > qgraph = qgraph.filter(feyn.filters.Depth(2))
    > qgraph.fit(data)
    """
    def __init__(self, depth):
        self.depth = depth

    def key(self):
        return "depth"

    def __call__(self, graphs:List[Graph]):
        return (g for g in graphs if g.depth == self.depth)

    def __repr__(self):
        return f"depth=={self.depth}"


class MaxDepth(QGraphFilter):
    """
    Use this class obtain a QGraph that only contain graphs up to a certain depth.
    
    # Consider only graphs with depth smaller or equal to 2
    > qgraph = qgraph.filter(feyn.filters.MaxDepth(2))
    > qgraph.fit(data)
    """
    def __init__(self, depth):
        self.depth = depth

    def key(self):
        return "depth"

    def __call__(self, graphs:List[Graph]):
        return (g for g in graphs if g.depth <= self.depth)

    def __repr__(self):
        return f"depth<={self.depth}"


class Edges(QGraphFilter):
    """
    Use this class obtain a QGraph that only contain graphs with a certain number of edges.
    
    # Consider only graphs with 3 edges
    > qgraph = qgraph.filter(feyn.filters.Edges(3))
    > qgraph.fit(data)
    """

    def __init__(self, edges):
        self.edges = edges

    def key(self):
        return "edges"

    def __call__(self, graphs:List[Graph]):
        return (g for g in graphs if g.edges == self.edges)

    def __repr__(self):
        return f"edges=={self.edges}"


class MaxEdges(QGraphFilter):
    """
    Use this class to obtain a QGraph that only contain graphs with a up to a certain number of edges.
    
    # Consider only graphs with up to 3 edges
    > qgraph = qgraph.filter(feyn.filters.MaxEdges(3))
    > qgraph.fit(data)
    """
    def __init__(self, edges):
        self.edges = edges

    def key(self):
        return "edges"

    def __call__(self, graphs:List[Graph]):
        return (g for g in graphs if g.edges <= self.edges)

    def __repr__(self):
        return f"edges<={self.edges}"


class Contains(QGraphFilter):
    """
    Use this class to obtain a QGraph that only contain graphs involving certain registers.
    
    # Consider only graphs that are two deep and involve the "x" register
    > qgraph = qgraph.filter(feyn.filters.Depth(2))
    > qgrpah = qgraph.filter(feyn.filters.Contains("x"))
    > qgraph.fit(data)

    Notice that this example demonstrates searching for all graphs that involve 'x' plus zero or one of the other input features.
    
    Using this chained filter approach it's possible to guide the search for non-linear and dynamic correlations in your dataset with the output variable.
    """
    def __init__(self, regname):
        self.regname = regname

    def key(self):
        return "contains_"+self.regname

    def __repr__(self):
        return f"\"{self.regname}\" in graph"

    def __call__(self, graphs:List[Graph]):
        return (g for g in graphs if self.regname in g) 
