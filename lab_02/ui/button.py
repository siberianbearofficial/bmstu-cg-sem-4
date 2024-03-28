from typing import Callable

from PyQtUIkit.widgets import KitButton, KitIconButton


class Button(KitButton):
    def __init__(self, label: str, on_click: Callable = None):
        super().__init__(label)
        self.setFixedHeight(40)

        if on_click:
            self.clicked.connect(on_click)


class IconButton(KitIconButton):
    def __init__(self, icon: str, on_click: Callable = None):
        super().__init__(icon)
        self.size = 45
        self.setContentsMargins(10, 10, 10, 10)

        if on_click:
            self.clicked.connect(on_click)
