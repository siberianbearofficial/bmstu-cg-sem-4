from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtWidgets import QWidget

from figures.line import Line
from figures.point import Point
from figures.triangle import Triangle


class Canvas(QWidget):
    def __init__(self, padding=20):
        super().__init__()
        self._painter = QPainter()

        self._camera_pos = (0, 0)
        self._scale = 1
        self.padding = padding

        self._points = []
        self._triangle = None
        self._intersection = None

        self.setMinimumSize(100, 100)

    def draw(self, points: list[Point], triangle: Triangle, intersection: Point):
        self._points = points
        self._triangle = triangle
        self._intersection = intersection
        self.scale()
        self.update()

    def paintEvent(self, a0) -> None:
        self._painter.begin(self)

        self._draw_line(Line.from_points(Point(0, 0), Point(0, 1)), '#00FF00')
        self._draw_line(Line.from_points(Point(0, 0), Point(1, 0)), '#00FF00')

        for el in self._points:
            self._draw_point(el, '#000000')
        if isinstance(self._triangle, Triangle):
            self._draw_triangle(self._triangle, '#0000FF')
        if isinstance(self._intersection, Point):
            self._draw_point(self._intersection, '#FF0000')

        self._painter.end()

    def resizeEvent(self, a0) -> None:
        self.scale()
        super().resizeEvent(a0)
        self.update()

    def scale(self):
        points = self._points
        triangle = self._triangle
        intersection = self._intersection
        if triangle is None or intersection is None:
            return

        min_x = min(0, *(p.x for p in points), intersection.x)
        max_x = max(0, *(p.x for p in points), intersection.x)
        min_y = min(0, *(p.y for p in points), intersection.y)
        max_y = max(0, *(p.y for p in points), intersection.y)
        self._camera_pos = (max_x + min_x) / 2, (max_y + min_y) / 2
        self._scale = min((self.width() - self.padding * 2) / (max_x - min_x), (self.height() - self.padding * 2) / (max_y - min_y))

    def _set_color(self, color):
        pen = QPen()
        pen.setColor(QColor(color))
        pen.setWidth(1)
        self._painter.setPen(pen)
        self._painter.setBrush(QColor(color))

    def _x(self, x):
        return int((x - self._camera_pos[0]) * self._scale + self.width() / 2)

    def _y(self, y):
        return int(-(y - self._camera_pos[1]) * self._scale + self.height() / 2)

    def _real_x(self, x):
        return (x + self._camera_pos[0] * self._scale - self.width() / 2) / self._scale

    def _real_y(self, y):
        return (-y + self._camera_pos[1] * self._scale + self.height() / 2) / self._scale

    def _draw_point(self, point: Point, color):
        self._set_color(color)
        self._painter.drawEllipse(QPoint(self._x(point.x), self._y(point.y)), 4, 4)
        self._painter.drawText(self._x(point.x), self._y(point.y) - 12, str(point))

    def _draw_line(self, line: Line, color):
        if not line.a:
            self._draw_segment(Point(self._real_x(0), line.y(0)),
                               Point(self._real_x(self.width()), line.y(0)),
                               color)
        else:
            self._draw_segment(Point(line.x(self._real_y(0)), self._real_y(0)),
                               Point(line.x(self._real_y(self.height())), self._real_y(self.height())),
                               color)

    def _draw_segment(self, p1, p2, color):
        self._set_color(color)
        self._painter.drawLine(self._x(p1.x), self._y(p1.y), self._x(p2.x), self._y(p2.y))

    def _draw_triangle(self, triangle: Triangle, color):
        self._draw_point(triangle.p1, color)
        self._draw_point(triangle.p2, color)
        self._draw_point(triangle.p3, color)
        self._draw_segment(triangle.p1, triangle.p2, color)
        self._draw_segment(triangle.p3, triangle.p2, color)
        self._draw_segment(triangle.p1, triangle.p3, color)

        self._draw_line(Line.from_points(triangle.p1, triangle.p2).perpendicular(triangle.p3), color)
        self._draw_line(Line.from_points(triangle.p1, triangle.p3).perpendicular(triangle.p2), color)
        self._draw_line(Line.from_points(triangle.p2, triangle.p3).perpendicular(triangle.p1), color)
