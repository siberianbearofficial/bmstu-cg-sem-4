from math import pi

from figures.arc import Arc
from figures.circle import Circle
from figures.point import Point
from figures.segment import Segment


class Tank:
    def __init__(self):
        self.objects = [
            # Main part
            Segment(Point(-20, -10), Point(-20, -20)),
            Segment(Point(-20, -20), Point(20, -20)),
            Segment(Point(20, -20), Point(20, -10)),
            Segment(Point(-30, -10), Point(30, -10)),
            Segment(Point(-30, 0), Point(30, 0)),
            Segment(Point(-20, -10), Point(-20, -20)),
            Segment(Point(-20, -10), Point(-20, -20)),
            Segment(Point(-20, -10), Point(-20, -20)),
            # Periscope
            Segment(Point(-11, -21.6), Point(-11, -27)),
            Segment(Point(-10, -21.65), Point(-10, -25)),
            Segment(Point(-11, -27), Point(-7, -27)),
            Segment(Point(-10, -25), Point(-7, -25)),
            Segment(Point(-7, -25), Point(-7, -27)),
            # Cabin
            Arc(Point(0, -20), 20, 2, pi, 2 * pi),
            # Semicircles
            Arc(Point(-30, -5), 5, 5, pi / 2, 3 * pi / 2),
            Arc(Point(30, -5), 5, 5, -pi / 2, pi / 2),
            # Wheels
            Circle(Point(-28, -5), 2.5),
            Circle(Point(-14, -5), 2.5),
            Circle(Point(0, -5), 2.5),
            Circle(Point(14, -5), 2.5),
            Circle(Point(28, -5), 2.5)
        ]

    def move(self, vector: Point):
        for obj in self.objects:
            obj.move(vector)
        return self

    def scale(self, p: Point, kx, ky):
        for obj in self.objects:
            obj.scale(p, kx, ky)
        return self

    def rotate(self, p: Point, angle):
        for obj in self.objects:
            obj.rotate(p, angle)
        return self
