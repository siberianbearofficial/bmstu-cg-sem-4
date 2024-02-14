from figures.line import Line


class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def heights_intersection(self):
        h1 = Line.from_points(self.p1, self.p2).perpendicular(self.p3)
        h2 = Line.from_points(self.p1, self.p3).perpendicular(self.p2)
        return h1.intersection(h2)


def find_triangle(points: list):
    max_sum = 0
    res = None
    for p1 in points:
        for p2 in points:
            if p1 == p2:
                continue
            for p3 in points:
                if p1 == p3 or p2 == p3:
                    continue

                tr = Triangle(p1, p2, p3)
                point = tr.heights_intersection()
                if sum(point) > max_sum:
                    max_sum = sum(point)
                    res = tr, point
    return res
