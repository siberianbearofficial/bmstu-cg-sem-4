"""
Лабораторная работа №2 по курсу "Компьютерная Графика"
Орлов Алексей (ИУ7-34Б)
"""

import sys
from math import radians

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, \
    QMessageBox, QApplication, QSizePolicy
from PyQtUIkit.widgets import *

from figures.point import Point
from figures.tank import Tank
from ui import SpinBox, Button

from canvas import Canvas


class MainWindow(KitMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Танк')
        self.setMinimumSize(1080, 720)

        layout = KitHBoxLayout()
        self.setCentralWidget(layout)

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        aside = KitVBoxLayout()
        aside.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        aside.setAlignment(Qt.AlignmentFlag.AlignTop)
        aside.setMaximumWidth(250)
        aside.setContentsMargins(0, 0, 0, 0)
        aside.setSpacing(20)
        layout.addWidget(aside)

        # MOVE
        move = KitVBoxLayout()
        move.setContentsMargins(0, 0, 0, 0)
        move.setSpacing(10)
        aside.addWidget(move)

        move.addWidget(KitLabel('Перемещение'))

        self.move_vector = Point(0, 0)
        move.addWidget(SpinBox('dx', self.move_vector.x, self.on_move_x_change))
        move.addWidget(SpinBox('dy', self.move_vector.y, self.on_move_y_change))

        move.addWidget(Button('Переместить', self.on_move_button_click))

        # SCALE
        scale = KitVBoxLayout()
        scale.setContentsMargins(0, 0, 0, 0)
        scale.setSpacing(10)
        aside.addWidget(scale)

        scale.addWidget(KitLabel('Масштабирование'))

        self.scale_point = Point(1, 1)
        scale.addWidget(SpinBox('x', self.scale_point.x, self.on_scale_x_change))
        scale.addWidget(SpinBox('y', self.scale_point.y, self.on_scale_y_change))

        self.scale_kx = 1
        scale.addWidget(SpinBox('kx', self.scale_kx, self.on_scale_kx_change))

        self.scale_ky = 1
        scale.addWidget(SpinBox('ky', self.scale_ky, self.on_scale_ky_change))

        scale.addWidget(Button('Масштабировать', self.on_scale_button_click))

        # ROTATE
        rotate = KitVBoxLayout()
        rotate.setContentsMargins(0, 0, 0, 0)
        rotate.setSpacing(10)
        aside.addWidget(rotate)

        rotate.addWidget(KitLabel('Вращение'))

        self.rotate_point = Point(0, 0)
        rotate.addWidget(SpinBox('x', self.rotate_point.x, self.on_rotate_x_change))
        rotate.addWidget(SpinBox('y', self.rotate_point.y, self.on_rotate_y_change))

        self.rotate_angle = 0
        rotate.addWidget(SpinBox('Угол', self.rotate_angle, self.on_rotate_angle_change))

        rotate.addWidget(Button('Вращать', self.on_rotate_button_click))

        main_widget = QWidget()
        main_widget_layout = QVBoxLayout(main_widget)
        main_widget_layout.setContentsMargins(0, 0, 0, 0)
        main_widget_layout.setSpacing(0)
        layout.addWidget(main_widget)

        self.tank = Tank()
        self.tank.scale(Point(0, 0), 10, 10)
        self.tank.move(400, 400)

        self.canvas = Canvas(20)
        main_widget_layout.addWidget(self.canvas)

        self.update_objects()

    def update_objects(self):
        # self.canvas.clear()
        self.canvas.draw(self.tank.objects)
        self.canvas.update()

    # MOVE

    def on_move_x_change(self, value):
        self.move_vector.x = value

    def on_move_y_change(self, value):
        self.move_vector.y = value

    def on_move_button_click(self):
        self.tank.move(self.move_vector.x, self.move_vector.y)
        self.update_objects()

    # SCALE

    def on_scale_x_change(self, value):
        self.scale_point.x = value

    def on_scale_y_change(self, value):
        self.scale_point.y = value

    def on_scale_kx_change(self, value):
        self.scale_kx = value

    def on_scale_ky_change(self, value):
        self.scale_ky = value

    def on_scale_button_click(self):
        if self.scale_kx == 0 or self.scale_ky == 0:
            MainWindow.error('Нельзя вводить ноль!')
        else:
            self.tank.scale(self.scale_point, self.scale_kx, self.scale_ky)
            self.update_objects()

    # ROTATE

    def on_rotate_x_change(self, value):
        self.rotate_point.x = value

    def on_rotate_y_change(self, value):
        self.rotate_point.y = value

    def on_rotate_angle_change(self, value):
        self.rotate_angle = value

    def on_rotate_button_click(self):
        self.tank.rotate(self.rotate_point, radians(self.rotate_angle))
        self.update_objects()

    @staticmethod
    def task():
        msgbox = QMessageBox()
        msgbox.setWindowTitle("Условие задачи")
        msgbox.setText("Отрисовать танк по координатам. Предоставить возможность перемещать, масштабировать и "
                       "вращать его относительно выбранных точек.")
        msgbox.exec()

    @staticmethod
    def error(msg: str):
        msgbox = QMessageBox()
        msgbox.setWindowTitle("Ошибка")
        msgbox.setText(msg)
        msgbox.exec()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
