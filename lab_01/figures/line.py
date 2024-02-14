from figures.point import Point


class Line:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def x(self, y):
        return (y * self.b + self.c) / -self.a

    def y(self, x):
        return (x * self.a + self.c) / -self.b

    def __str__(self):
        return f"{self.a:3g} * x + {self.b:3g} * y + {self.c:3g} == 0"

    def perpendicular(self, point: Point):
        a = self.b
        b = -self.a
        c = -a * point.x - b * point.y
        return Line(a, b, c)

    def intersection(self, other):
        c = -self.c
        f = -other.c
        p = self.a * other.b - other.a * self.b
        x = (c * other.b - self.b * f) / p
        y = (self.a * f - c * other.a) / p

        return Point(x, y)

    @staticmethod
    def from_points(p1: Point, p2: Point):
        a = p2.y - p1.y
        b = p1.x - p2.x
        c = -a * p1.x - b * p1.y
        return Line(a, b, c)


if __name__ == '__main__':
    l1 = Line.from_points(Point(1, 1), Point(5, 5))
    l2 = Line.from_points(Point(4, 2), Point(2, 4))
    print(l1)
    print(l2)
    print(tuple(l1.intersection(l2)))
