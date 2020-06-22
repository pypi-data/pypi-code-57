from lalgebra.point import Point
from lalgebra.line import Line

class InvalidPolygonError(Exception):
    pass

class Polygon:
    vertices = []
    area = property(lambda self: sum([self.vertices[v] + self.vertices[v+1] for v in range(0, len(self.vertices)-1)]) + sum([-1*(self.vertices[v] + self.vertices[v-1]) for v in range(1, len(self.vertices))]))

    def __init__(self, vertices):
        if len(vertices) < 3: raise InvalidPolygonError("A polygon must have at least 3 vertices!")
        self.vertices = vertices