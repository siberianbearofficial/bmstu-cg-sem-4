from typing import Callable

from PyQt6.QtCore import Qt
from PyQtUIkit.widgets import KitButton


class Button(KitButton):
    def __init__(self, label: str, on_click: Callable = None):
        super().__init__(label)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        if on_click:
            self.clicked.connect(on_click)
