from figures.point import Point


class Segment:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return f'[{self.p1}, {self.p2}]'

    def move(self, dx=0, dy=0):
        self.p1.move(dx, dy)
        self.p2.move(dx, dy)

    def scale(self, p: Point, kx=1, ky=1):
        self.p1.scale(p, kx, ky)
        self.p2.scale(p, kx, ky)
