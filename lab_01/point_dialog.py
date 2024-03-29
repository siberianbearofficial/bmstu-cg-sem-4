from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDoubleSpinBox, QHBoxLayout, QPushButton


class PointDialog(QDialog):
    def __init__(self, x=0, y=0):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Ввод X:"))

        self._x_edit = QDoubleSpinBox()
        self._x_edit.setRange(-1e300, 1e300)
        self._x_edit.setValue(float(x))
        layout.addWidget(self._x_edit)

        layout.addWidget(QLabel("Ввод Y:"))

        self._y_edit = QDoubleSpinBox()
        self._y_edit.setRange(-1e300, 1e300)
        self._y_edit.setValue(float(y))
        layout.addWidget(self._y_edit)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(buttons_layout)

        self._button_ok = QPushButton("Ок")
        self._button_ok.clicked.connect(self.accept)
        buttons_layout.addWidget(self._button_ok)

        self._button_cancel = QPushButton("Отмена")
        self._button_cancel.clicked.connect(self.reject)
        buttons_layout.addWidget(self._button_cancel)

        self._x_edit.selectAll()

    @property
    def res(self):
        return self._x_edit.value(), self._y_edit.value()
