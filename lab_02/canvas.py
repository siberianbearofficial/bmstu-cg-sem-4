from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtWidgets import QWidget, QSizePolicy

from figures.arc import Arc
from figures.ellipse import Ellipse
from figures.point import Point
from figures.segment import Segment


class Canvas(QWidget):
    def __init__(self, padding=20):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._painter = QPainter()

        self.padding = padding

        self._objects = list()

        self.setMinimumSize(100, 100)

        self.primary_color = QColor(0, 0, 0, 255)

    def draw(self, objects):
        self._objects.clear()
        self._objects.extend(objects)
        self.update()

    def paintEvent(self, a0) -> None:
        super().paintEvent(a0)
        self._painter.begin(self)

        for el in self._objects:
            if isinstance(el, Segment):
                self._draw_segment(el.p1, el.p2, self.primary_color)
            elif isinstance(el, Point):
                self._draw_point(el, self.primary_color)
            elif isinstance(el, Arc):
                for segment in el.segments:
                    self._draw_segment(segment.p1, segment.p2, self.primary_color)

        self._painter.end()

    def _set_color(self, color):
        pen = QPen()
        pen.setColor(QColor(color))
        pen.setWidth(1)
        self._painter.setPen(pen)
        self._painter.setBrush(QColor(color))

    def _draw_point(self, point: Point, color):
        self._set_color(color)
        self._painter.drawEllipse(int(point.x), int(point.y), 2, 2)
        self._painter.drawText(int(point.x), int(point.y) - 12, str(point))

    def _draw_segment(self, p1, p2, color):
        self._set_color(color)
        self._painter.drawLine(int(p1.x), int(p1.y), int(p2.x), int(p2.y))
