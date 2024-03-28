from math import sin, cos


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        yield self.x
        yield self.y

    def __str__(self):
        x = self.x if isinstance(self.x, int) else f'{self.x:.4g}'.strip()
        y = self.y if isinstance(self.y, int) else f'{self.y:.4g}'.strip()
        return f"({x}, {y})"

    def move(self, vector: 'Point'):
        self.x += vector.x
        self.y += vector.y
        return self

    def scale(self, p: 'Point', kx=1, ky=1):
        self.x = (self.x - p.x) * kx + p.x
        self.y = (self.y - p.y) * ky + p.y
        return self

    def rotate(self, p: 'Point', angle=0):
        x = (self.x - p.x) * cos(angle) - (self.y - p.y) * sin(angle) + p.x
        y = (self.x - p.x) * sin(angle) + (self.y - p.y) * cos(angle) + p.y
        self.x = x
        self.y = y
        return self

    def clone(self):
        return Point(self.x, self.y)
