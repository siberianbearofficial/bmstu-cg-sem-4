from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtWidgets import QWidget, QSizePolicy

from figures.line import Line
from figures.point import Point
from figures.triangle import Triangle


class Canvas(QWidget):
    def __init__(self, padding=20):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._painter = QPainter()

        self._camera_pos = (0, 0)
        self._scale = 1
        self.padding = padding

        self._points = []
        self._triangle = None
        self._point = None
        self._bisector = None
        self._height = None

        self.setMinimumSize(100, 100)

    def draw(self, points: list[Point], point: Point, triangle: Triangle, bisector: Line, height: Line):
        self._points = points
        self._triangle = triangle
        self._point = point
        self._bisector = bisector
        self._height = height
        self.scale()
        self.update()

    def paintEvent(self, a0) -> None:
        self._painter.begin(self)

        self._draw_line(Line.from_points(Point(0, 0), Point(0, 1)), QColor(0, 0, 0, 150))
        self._draw_line(Line.from_points(Point(0, 0), Point(1, 0)), QColor(0, 0, 0, 150))

        for el in self._points:
            self._draw_point(el, '#122faa')
        if isinstance(self._triangle, Triangle):
            self._draw_triangle(self._triangle, self._point, self._bisector, self._height, '#7200a3')

        self._painter.end()

    def resizeEvent(self, a0) -> None:
        self.scale()
        super().resizeEvent(a0)
        self.update()

    def scale(self):
        min_y, max_y, min_x, max_x = 0, 0, 0, 0
        for point in self._points:
            if point.y < min_y:
                min_y = point.y
            if point.y > max_y:
                max_y = point.y
            if point.x < min_x:
                min_x = point.x
            if point.x > max_x:
                max_x = point.x

        self._camera_pos = (max_x + min_x) / 2, (max_y + min_y) / 2
        if max_x - min_x < 1e-6 or max_y - min_y < 1e-6:
            self._scale = 1
        else:
            self._scale = min((self.height() - self.padding * 2) / (max_y - min_y),
                              (self.width() - self.padding * 2) / (max_x - min_x))

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
        self._painter.drawEllipse(QPoint(self._x(point.x), self._y(point.y)), 2, 2)
        self._painter.drawText(self._x(point.x), self._y(point.y) - 12, str(point))

    def _draw_line(self, line: Line, color):
        if line.a:
            self._draw_segment(Point(line.x(self._real_y(0)), self._real_y(0)),
                               Point(line.x(self._real_y(self.height())), self._real_y(self.height())),
                               color)
        else:
            self._draw_segment(Point(self._real_x(0), line.y(0)),
                               Point(self._real_x(self.width()), line.y(0)),
                               color)

    def _draw_segment(self, p1, p2, color):
        self._set_color(color)
        self._painter.drawLine(self._x(p1.x), self._y(p1.y), self._x(p2.x), self._y(p2.y))

    def _draw_triangle(self, triangle: Triangle, point: Point, bisector: Line, height: Line, color):
        accent_color = '#c154c1'

        self._draw_segment(triangle.p1, triangle.p2, color)
        self._draw_segment(triangle.p3, triangle.p2, color)
        self._draw_segment(triangle.p1, triangle.p3, color)

        self._draw_point(triangle.p1, accent_color if triangle.p1 == point else color)
        self._draw_point(triangle.p2, accent_color if triangle.p2 == point else color)
        self._draw_point(triangle.p3, accent_color if triangle.p3 == point else color)

        self._draw_line(height, accent_color)
        self._draw_line(bisector, accent_color)
