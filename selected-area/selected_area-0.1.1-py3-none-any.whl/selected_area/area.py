from __future__ import annotations
from typing import NamedTuple, Optional, Tuple


class Point(NamedTuple):
    x: float
    y: float


class Segment:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def line(self) -> Tuple[float, float, float]:
        a = self.p1.y - self.p2.y
        b = self.p2.x - self.p1.x
        c = self.p1.x * self.p2.y - self.p2.x * self.p1.y
        return a, b, -c

    def intersection_point(self, segment2: Segment) -> Optional[Point]:
        line1 = self.line()
        line2 = segment2.line()
        d = line1[0] * line2[1] - line1[1] * line2[0]
        dx = line1[2] * line2[1] - line1[1] * line2[2]
        dy = line1[0] * line2[2] - line1[2] * line2[0]
        if d != 0:
            x = dx / d
            y = dy / d
            return Point(x, y)

    def __repr__(self):
        return f'Segment(p1={self.p1!r}, p2={self.p2!r})'


class SelectedArea:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def point_inside(self, point: Point) -> bool:
        return self.p1.x <= point.x <= self.p2.x and self.p1.y <= point.y <= self.p2.y

    def crossing_line(self, segment: Segment) -> bool:
        plot1 = Segment(self.p1, Point(self.p2.x, self.p1.y))
        plot2 = Segment(Point(self.p1.x, self.p2.y), self.p2)
        intersections = [plot1.intersection_point(segment), plot2.intersection_point(segment)]
        for intersection in intersections:
            if intersection and self.point_inside(intersection):
                return True
        return False

    def contains(self, segment: Segment) -> bool:
        points = [segment.p1, segment.p2]
        for point in points:
            if self.point_inside(point):
                return True
        return self.crossing_line(segment)
