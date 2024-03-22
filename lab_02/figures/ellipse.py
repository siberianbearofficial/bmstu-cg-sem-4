from math import pi

from figures.arc import Arc
from figures.point import Point


class Ellipse(Arc):
    def __init__(self, center: Point, radius1, radius2):
        super().__init__(center, radius1, radius2, 0, 2 * pi)
