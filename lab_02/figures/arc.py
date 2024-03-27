from math import cos, sin, pi

from figures.point import Point
from figures.segment import Segment


class Arc:
    def __init__(self, center: Point, radius1, radius2, angle1, angle2):
        self.center = center
        self.radius1 = radius1
        self.radius2 = radius2
        self.angle = 0
        self.angle1 = angle1
        self.angle2 = angle2

    def move(self, dx=0, dy=0):
        self.center.move(dx, dy)

    def scale(self, p: Point, kx=1, ky=1):
        self.center.scale(p, kx, ky)
        self.radius1 *= kx
        self.radius2 *= ky

    def rotate(self, p: Point, angle):
        self.center.rotate(p, angle)
        self.angle += angle

    @property
    def segments(self):
        step = 1 / min(self.radius1, self.radius2)
        prev = Point(self.radius1 * cos(self.angle1),
                     self.radius2 * sin(self.angle1)).move(*self.center).rotate(self.center, self.angle)
        angle = self.angle1 + step
        while angle < self.angle2:
            point = Point(self.radius1 * cos(angle),
                          self.radius2 * sin(angle)).move(*self.center).rotate(self.center, self.angle)
            angle += step
            yield Segment(prev, point)
            prev = point
        yield Segment(prev, Point(self.radius1 * cos(self.angle2),
                                  self.radius2 * sin(self.angle2)).move(*self.center).rotate(self.center, self.angle))
