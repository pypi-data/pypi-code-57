from point import Point
from line import Line
from vector import Vector
import math

class InvalidPolygonError(Exception):
    pass

class Polygon:
    vertices = []
    __calc = property(lambda self: self.vertices + [self.vertices[0]])
    area = property(lambda self: 0.5 * (sum([self.__calc[v].x * self.__calc[v+1].y for v in range(0, len(self.__calc)-1)]) + sum([-1*(self.__calc[v].x * self.__calc[v-1].y) for v in range(1, len(self.__calc))])))
    centroid = property(lambda self: Vector(sum([a.x for a in self.vertices])/len(self.vertices),sum([a.y for a in self.vertices])/len(self.vertices)))

    def __init__(self, vertices):
        if len(vertices) < 3: raise InvalidPolygonError("A polygon must have at least 3 vertices!")
        self.vertices = vertices
        l = [[math.atan2(a.y - self.centroid.y, a.x - self.centroid.x), a] for a in vertices]
        l.sort()
        self.vertices = [a[1] for a in l]