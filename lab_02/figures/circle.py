from figures.ellipse import Ellipse
from figures.point import Point


class Circle(Ellipse):
    def __init__(self, center: Point, radius):
        super().__init__(center, radius, radius)
