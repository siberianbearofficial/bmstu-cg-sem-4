from math import fabs, sqrt


class NoTriangleException(Exception):
    pass


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        eps = 1e-6
        return fabs(self.x - other.x) < eps and fabs(self.y - other.y) < eps


class Triangle:
    def __init__(self, p1, p2, p3):
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

    def __res(self, s1, s2, s3):
        """
        Промежуточный результат
        :param s1: BC
        :param s2: AC
        :param s3: AB
        :return:
        """
        return s3 * s2 / (s3 + s1) - sqrt(s3 ** 2 - (2 * self.area / s2) ** 2)

    def res(self):
        res1 = self.__res(self.s3, self.s1, self.s2)
        res2 = self.__res(self.s1, self.s2, self.s3)
        res3 = self.__res(self.s2, self.s3, self.s1)

        if res1 > res2 and res1 > res3:
            return res1, self.p1
        if res2 > res1 and res2 > res3:
            return res2, self.p2
        return res3, self.p3


class Points:
    def __init__(self, points, canvas):
        self.points = points
        self.res_triangle = None
        self.canvas = canvas
        self.scale = 1

    def draw_res(self):
        point, self.res_triangle = self.find_points()

        # self.adjust()

        self.canvas.draw(self.points, self.res_triangle, None)

        # self.canvas.draw_triangle(self.res_triangle.p1.x, self.res_triangle.p1.y,
        #                           self.res_triangle.p2.x, self.res_triangle.p2.y,
        #                           self.res_triangle.p3.x, self.res_triangle.p3.y, (255, 0, 0), 3)
        #
        # for point in self.points:
        #     self.canvas.draw_point(self.to_screen_x(point.x), self.to_screen_y(point.y), self.to_screen_x(point.x_draw), point.y_draw, point.num, color, 5)

    # def adjust(self):
    #     min_y, max_y, min_x, max_x = 0, 0, 0, 0
    #     for point in self.points:
    #         if point.y < min_y:
    #             min_y = point.y
    #         if point.y > max_y:
    #             max_y = point.y
    #         if point.x < min_x:
    #             min_x = point.x
    #         if point.x > max_x:
    #             max_x = point.x
    #
    #     self.scale = min((self.canvas.height() - self.padding * 2) / (max_y - min_y),
    #                      (self.canvas.width() - self.padding * 2) / (max_x - min_x))

    def find_points(self):
        max_result = None
        max_triangle = None
        max_point = None

        for i in range(len(self.points) - 2):
            for j in range(i + 1, len(self.points) - 1):
                for k in range(j + 1, len(self.points)):
                    try:
                        t = Triangle(self.points[i], self.points[j], self.points[k])

                        result, point = t.res()
                        if not max_result or result > max_result:
                            max_result = result
                            max_triangle = t
                            max_point = point
                    except:
                        pass

        if not max_triangle:
            raise NoTriangleException

        return max_point, max_triangle
