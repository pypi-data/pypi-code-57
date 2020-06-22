from lalgebra.point import Point
from lalgebra.line import Line

class InvalidPolygonError(Exception):
    pass

class Polygon:
    vertices = []
    calc = property(lambda self: self.vertices + [self.vertices[0]])
    area = property(lambda self: 0.5 * (sum([self.calc[v].x * self.calc[v+1].y for v in range(0, len(self.calc)-1)]) + sum([-1*(self.calc[v].x * self.calc[v-1].y) for v in range(1, len(self.calc))])))

    def __init__(self, vertices):
        if len(vertices) < 3: raise InvalidPolygonError("A polygon must have at least 3 vertices!")
        self.vertices = vertices