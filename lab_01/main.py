"""
Лабораторная работа №1 по курсу "Компьютерная Графика"
Орлов Алексей (ИУ7-34Б)
"""

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, \
    QMessageBox, QApplication, QSizePolicy, QLabel

from canvas import Canvas
from point_dialog import PointDialog
from points_table import PointsTable

from figures.point import Point
from figures.triangle import Triangle, NoTriangleException


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Треугольники')
        self.setMinimumSize(1080, 720)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        aside = QWidget()
        aside.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        aside.setMaximumWidth(400)
        aside_layout = QVBoxLayout(aside)
        aside_layout.setContentsMargins(0, 0, 0, 0)
        aside_layout.setSpacing(20)
        layout.addWidget(aside)

        buttons = QWidget()
        buttons_layout = QHBoxLayout(buttons)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(10)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        aside_layout.addWidget(buttons)

        self.task_button = QPushButton('📓')
        self.task_button.setStyleSheet('background-color: rgba(0, 0, 255, 0.1); border: none; border-radius: 5px;')
        self.task_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.task_button.setFixedSize(40, 40)
        self.task_button.clicked.connect(self.task)
        buttons_layout.addWidget(self.task_button)

        self.add_point_button = QPushButton('Добавить точку ➕')
        self.add_point_button.setStyleSheet('background-color: rgba(150, 100, 255, 0.1); border: none; border-radius: 5px; padding-left: 10px; padding-right: 10px;')
        self.add_point_button.setFixedHeight(40)
        self.add_point_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_point_button.clicked.connect(self.add)
        buttons_layout.addWidget(self.add_point_button)

        self.run_button = QPushButton('Построить 🖊')
        self.run_button.setStyleSheet('background-color: rgba(150, 100, 255, 0.1); border: none; border-radius: 5px; padding-left: 10px; padding-right: 10px;')
        self.run_button.setFixedHeight(40)
        self.run_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.run_button.clicked.connect(self.find)
        buttons_layout.addWidget(self.run_button)

        self.points_table = PointsTable()
        aside_layout.addWidget(self.points_table)

        self.clear_button = QPushButton('🧹')
        self.clear_button.setStyleSheet('background-color: rgba(255, 150, 0, 0.1); border: none; border-radius: 5px;')
        self.clear_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_button.setFixedSize(40, 40)
        self.clear_button.clicked.connect(self.points_table.clear)
        buttons_layout.addWidget(self.clear_button)

        self.result_label = QLabel()
        aside_layout.addWidget(self.result_label)

        main_widget = QWidget()
        main_widget.setStyleSheet('background-color: rgba(255, 255, 255, 0.1); border-radius: 5px;')
        main_widget_layout = QVBoxLayout(main_widget)
        main_widget_layout.setContentsMargins(0, 0, 0, 0)
        main_widget_layout.setSpacing(0)
        layout.addWidget(main_widget)

        self.canvas = Canvas(20)
        main_widget_layout.addWidget(self.canvas)

    def add(self):
        dialog = PointDialog()
        if dialog.exec():
            self.points_table.add(Point(*dialog.res))

    @staticmethod
    def task():
        msgbox = QMessageBox()
        msgbox.setWindowTitle("Условие задачи")
        msgbox.setText("На плоскости дано множество точек. Найти такой треугольник с вершинами " +
                       "в этих точках, для которого угол между биссектрисой и высотой, проведенных из одной точки, "
                       "максимален. При этом учитывается наибольший такой угол из всех вершин каждого треугольника.")
        msgbox.exec()

    def find(self):
        self.canvas.shapes = []
        points = []
        for point in self.points_table.points:
            x = float(point.x)
            y = float(point.y)
            p = Point(x, y)
            if p not in points:
                points.append(p)

        if len(points) < 3:
            self.not_enough_points()
        else:
            try:
                max_point, max_triangle, max_bisector, max_height, max_bisector_height_angle = Triangle.with_max_bisector_height_angle(points)
                self.canvas.draw(points, max_point, max_triangle, max_bisector, max_height)
                self.result_label.setText(f'Результат:\n'
                                          f'Треугольник: '
                                          f'{points.index(max_triangle.p1) + 1} - {max_triangle.p1}, '
                                          f'{points.index(max_triangle.p2) + 1} - {max_triangle.p2}, '
                                          f'{points.index(max_triangle.p3) + 1} - {max_triangle.p3}\n'
                                          f'Вершина: {max_point}\n'
                                          f'Угол: {max_bisector_height_angle:.2f} рад.')
            except NoTriangleException:
                self.no_triangle()
                self.result_label.setText('Результат не найден.')

    @staticmethod
    def not_enough_points():
        msgbox = QMessageBox()
        msgbox.setText("Необходимо задать хотя бы три различные точки.")
        msgbox.exec()

    @staticmethod
    def no_triangle():
        msgbox = QMessageBox()
        msgbox.setText("Треугольники вырожденные.")
        msgbox.exec()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
