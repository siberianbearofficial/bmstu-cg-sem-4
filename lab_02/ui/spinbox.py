from typing import Callable

from PyQtUIkit.widgets import KitHBoxLayout, KitLabel, KitSpinBox


class SpinBox(KitHBoxLayout):
    def __init__(self, label: str, value: int = 0, on_change: Callable = None):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(10)

        self.addWidget(KitLabel(label))

        self.value = value
        self._on_change = on_change

        self._spinbox = KitSpinBox(float)
        self._spinbox.setValue(value)
        self._spinbox.valueChanged.connect(self._value_changed)
        self.addWidget(self._spinbox)

    def _value_changed(self, value):
        self.value = value
        self._on_change(value)
