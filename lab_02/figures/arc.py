from math import cos, sin

from figures.point import Point
from figures.segment import Segment


class Arc:
    def __init__(self, center: Point, radius1, radius2, angle1, angle2):
        if not radius1 or not radius2:
            raise ValueError('Radius cannot be zero')

        self.segments = []
        step = 1 / 100  # 1 / min(radius1, radius2)
        prev = Point(radius1 * cos(angle1),
                     radius2 * sin(angle1)).move(center)
        angle = angle1 + step
        while angle < angle2:
            point = Point(radius1 * cos(angle),
                          radius2 * sin(angle)).move(center)
            angle += step
            self.segments.append(Segment(prev, point))
            prev = point
        self.segments.append(Segment(prev, Point(radius1 * cos(angle2), radius2 * sin(angle2)).move(center)))

    def move(self, vector: Point):
        self.segments[0].p1.move(vector)
        for i in range(len(self.segments)):
            self.segments[i].p2.move(vector)

    def scale(self, p: Point, kx=1, ky=1):
        self.segments[0].p1.scale(p, kx, ky)
        for i in range(len(self.segments)):
            self.segments[i].p2.scale(p, kx, ky)
        return self

    def rotate(self, p: Point, angle):
        self.segments[0].p1.rotate(p, angle)
        for i in range(len(self.segments)):
            self.segments[i].p2.rotate(p, angle)
        return self

    # @property
    # def segments(self):
    #     step = 1 / min(self.radius1, self.radius2) if (self.radius1 and self.radius2) else 100000
    #     prev = Point(self.radius1 * cos(self.angle1),
    #                  self.radius2 * sin(self.angle1)).move(*self.center).rotate(self.center, self.angle)
    #     angle = self.angle1 + step
    #     while angle < self.angle2:
    #         point = Point(self.radius1 * cos(angle),
    #                       self.radius2 * sin(angle)).move(*self.center).rotate(self.center, self.angle)
    #         angle += step
    #         yield Segment(prev, point)
    #         prev = point
    #     yield Segment(prev, Point(self.radius1 * cos(self.angle2),
    #                               self.radius2 * sin(self.angle2)).move(*self.center).rotate(self.center, self.angle))
