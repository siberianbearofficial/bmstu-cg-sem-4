from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QSizePolicy, QSpacerItem, \
    QScrollArea

from point_dialog import PointDialog
from figures.point import Point


class PointsTableRow(QWidget):
    def __init__(self, point: Point, on_delete):
        super().__init__()
        self.setFixedHeight(40)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.point = point

        self.x_label = QLabel(f'{point.x:.2f}')
        self.x_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.x_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addWidget(self.x_label)

        self.y_label = QLabel(f'{point.y:.2f}')
        self.y_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.y_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addWidget(self.y_label)

        delete_button = QPushButton('✖️')
        delete_button.setStyleSheet('background-color: rgba(255, 255, 255, 0);')
        delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_button.clicked.connect(lambda: on_delete(self))
        delete_button.setFixedWidth(30)
        layout.addWidget(delete_button)

    def mouseDoubleClickEvent(self, a0):
        super().mouseDoubleClickEvent(a0)
        dialog = PointDialog(self.point.x, self.point.y)
        if dialog.exec():
            self.point.x, self.point.y = dialog.res
            self.x_label.setText(f'{self.point.x:.2f}')
            self.y_label.setText(f'{self.point.y:.2f}')


class PointsTable(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.points = []

        header = QWidget()
        header.setStyleSheet('font-weight: bold; border-bottom: 1px solid rgba(0, 0, 0, 0.5)')
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        layout.addWidget(header)

        self._scroll_area = QScrollArea()
        self._scroll_area.setStyleSheet('border: none;')
        self._scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout.addWidget(self._scroll_area)
        points = QWidget()
        self._scroll_area.setWidget(points)
        self._scroll_area.setWidgetResizable(True)
        self.points_layout = QVBoxLayout(points)
        self.points_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.points_layout.setContentsMargins(0, 0, 0, 0)
        self.points_layout.setSpacing(0)

        x_label = QLabel('X')
        x_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        x_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(x_label)

        y_label = QLabel('Y')
        y_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        y_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(y_label)

        spacer = QSpacerItem(30, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        header_layout.addItem(spacer)

    def add(self, point: Point):
        row = PointsTableRow(point, self.remove)
        self.points.append(point)
        self.points_layout.addWidget(row)

    def remove(self, row: PointsTableRow):
        point = row.point
        self.points.remove(point)
        self.points_layout.removeWidget(row)
        row.setParent(None)
        return point

    def clear(self):
        for _ in range(self.points_layout.count()):
            self.points_layout.takeAt(0).widget().setParent(None)
        self.points.clear()
