from math import sqrt, atan
from figures.line import Line
from figures.point import Point


class NoTriangleException(Exception):
    pass


class Triangle:
    def __init__(self, p1: Point, p2: Point, p3: Point):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        self.s1 = sqrt((p3.x - p2.x) ** 2 + (p3.y - p2.y) ** 2)
        self.s2 = sqrt((p3.x - p1.x) ** 2 + (p3.y - p1.y) ** 2)
        self.s3 = sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

        p = (self.s1 + self.s2 + self.s3) / 2
        self.area = sqrt(p * (p - self.s1) * (p - self.s2) * (p - self.s3))

        if self.area < 1e-6:
            raise NoTriangleException

    def height(self, point: Point):
        match point:
            case self.p1:
                return Line.from_points(self.p2, self.p3).perpendicular(self.p1)
            case self.p2:
                return Line.from_points(self.p1, self.p3).perpendicular(self.p2)
            case _:
                return Line.from_points(self.p1, self.p2).perpendicular(self.p3)

    def __bisector_height_angle(self, point: Point):
        """
        Угол между биссектрисой и высотой из вершины point.
        :param point: вершина для нахождения угла.
        :return: найденный угол, биссектриса и высота из вершины point.
        """

        points = [self.p1, self.p2, self.p3]
        points.remove(point)

        height = Line.from_points(*points).perpendicular(point)

        a, b = points[0], points[1]
        a_point_len = sqrt((a.x - point.x) ** 2 + (a.y - point.y) ** 2)
        b_point_len = sqrt((b.x - point.x) ** 2 + (b.y - point.y) ** 2)
        p = Point(point.x + (b.x - point.x) / b_point_len * a_point_len,
                  point.y + (b.y - point.y) / b_point_len * a_point_len)
        line_a_perp = Line.from_points(point, a).perpendicular(a)
        line_b_perp = Line.from_points(point, b).perpendicular(p)
        line_ab = Line.from_points(a, b)

        bisector = Line.from_points(point, line_a_perp.intersection(line_b_perp))

        p1 = bisector.intersection(line_ab)
        p2 = height.intersection(line_ab)
        p12_distance = sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
        height_distance = sqrt((point.x - p2.x) ** 2 + (point.y - p2.y) ** 2)

        return atan(p12_distance / height_distance), bisector, height

    def max_bisector_height_angle(self):
        """
        Максимальный угол между биссектрисой и высотой.
        :return: найденный угол, вершина, биссектриса и высота из этой вершины.
        """

        res1, bis1, hgt1 = self.__bisector_height_angle(self.p1)
        res2, bis2, hgt2 = self.__bisector_height_angle(self.p2)
        res3, bis3, hgt3 = self.__bisector_height_angle(self.p3)

        if res1 > res2 and res1 > res3:
            return res1, self.p1, bis1, hgt1
        if res2 > res1 and res2 > res3:
            return res2, self.p2, bis2, hgt2
        return res3, self.p3, bis3, hgt3

    @staticmethod
    def with_max_bisector_height_angle(points: list[Point]):
        max_bisector_height_angle = None
        max_triangle = None
        max_point = None
        max_bisector = None
        max_height = None

        for i in range(len(points) - 2):
            for j in range(i + 1, len(points) - 1):
                for k in range(j + 1, len(points)):
                    try:
                        triangle = Triangle(points[i], points[j], points[k])

                        bisector_height_angle, point, bisector, height = triangle.max_bisector_height_angle()
                        if not max_bisector_height_angle or bisector_height_angle > max_bisector_height_angle:
                            max_bisector_height_angle = bisector_height_angle
                            max_triangle = triangle
                            max_point = point
                            max_bisector = bisector
                            max_height = height
                    except NoTriangleException:
                        pass

        if not max_triangle:
            raise NoTriangleException

        return max_point, max_triangle, max_bisector, max_height
