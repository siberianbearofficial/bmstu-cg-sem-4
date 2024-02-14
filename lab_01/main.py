import sys
from PyQt6.QtWidgets import QTableWidgetItem, QMainWindow, QTableWidget, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, \
    QMessageBox, QApplication

from canvas import Canvas
from point_dialog import PointDialog
from points import Points, Point, NoTriangleException


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(1080, 720)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)

        aside = QWidget()
        aside.setMinimumWidth(300)
        aside.setMaximumWidth(500)
        aside_layout = QVBoxLayout(aside)
        layout.addWidget(aside)

        self.add_point_button = QPushButton()
        self.add_point_button.clicked.connect(self.add_point)
        aside_layout.addWidget(self.add_point_button)

        self.task_button = QPushButton()
        self.task_button.clicked.connect(self.task)
        aside_layout.addWidget(self.task_button)

        self.run_button = QPushButton()
        self.run_button.clicked.connect(self.find)
        aside_layout.addWidget(self.run_button)

        self.points_table = QTableWidget()
        self.points_table.setRowCount(0)
        self.points_table.setColumnCount(2)
        self.points_table.horizontalHeader().setDefaultSectionSize(150)
        self.points_table.setHorizontalHeaderLabels(['x', 'y'])
        aside_layout.addWidget(self.points_table)

        # self.del_button = QPushButton()
        # self.del_button.clicked.connect(self.del_point)
        # aside_layout.addWidget(self.del_button)

        self.canvas = Canvas(20)
        layout.addWidget(self.canvas)

    def add_point(self):
        dialog = PointDialog()
        if dialog.exec():
            x, y = dialog.res
            self.points_table.insertRow(self.points_table.rowCount())
            self.points_table.setItem(self.points_table.rowCount() - 1, 0,
                                      QTableWidgetItem(str(x)))
            self.points_table.setItem(self.points_table.rowCount() - 1, 1,
                                      QTableWidgetItem(str(y)))

    def task(self):
        msgbox = QMessageBox()
        msgbox.setWindowTitle("Условие")
        msgbox.setText("На плоскости дано множество точек. Найти такой треугольник с вершинами " +
                       "в этих точках, для которого разность количеств точек попавших внутрь треугольника "
                       "и за его пределы, но внутри описанной окружности, минимальна")
        msgbox.exec()

    def find(self):
        self.canvas.shapes = []
        points = []
        for num in range(1, self.points_table.rowCount() + 1):
            x = float(self.points_table.item(num - 1, 0).text())
            y = float(self.points_table.item(num - 1, 1).text())
            p = Point(x, y)
            if p not in points:
                points.append(p)

        if len(points) < 3:
            self.not_enough_points()

            return None

        field = Points(points, self.canvas)

        try:
            field.draw_res()
        except NoTriangleException:
            self.no_triangle()

    def not_enough_points(self):
        msgbox = QMessageBox()
        msgbox.setText("Минимальное число разных точек - 3")
        msgbox.exec()

    def no_triangle(self):
        msgbox = QMessageBox()
        msgbox.setText("Все треугольники вырожденные")
        msgbox.exec()


def main():
    app = QApplication(sys.argv)
    window = App()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
