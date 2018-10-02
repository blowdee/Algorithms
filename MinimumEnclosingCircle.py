import math
import random
import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

VAL_FROMRAND = 0
VAL_FROMINPUT = 1
DEF_N = 30


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.groupboxes = [None] * 2
        self.cur_mode = None
        self.init_ui()

    def init_ui(self):
        window_size = (580, 540)
        self.resize(*window_size)
        self.setWindowTitle('Minimum enclosing circle')
        self.center()
        self.populate_ui()
        self.show()

    def center(self):
        fg = self.frameGeometry()
        fg.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(fg.topLeft())

    def populate_ui(self):
        def add_groupbox(title, value, layout):
            def on_group_checked(checked):
                cur_gbox = self.sender()
                blockers = []
                if checked:
                    for gbox in self.groupboxes:
                        blockers.append(QSignalBlocker(gbox))
                        gbox.setChecked(False)
                        for child in gbox.children:
                            child.setEnabled(False)
                cur_gbox.setChecked(True)
                self.cur_mode = cur_gbox.value
                for child in cur_gbox.children:
                    child.setEnabled(True)

            groupbox = QGroupBox(title)
            groupbox.value = value
            groupbox.children = []
            groupbox.setCheckable(True)
            groupbox.setChecked(False)
            groupbox.toggled.connect(on_group_checked)
            layout.addWidget(groupbox)
            self.groupboxes[value] = groupbox

        layout = QVBoxLayout()
        widget = QWidget(self)
        widget.setLayout(layout)

        add_groupbox('Generate random', VAL_FROMRAND, layout)
        self.populate_groupbox(VAL_FROMRAND)
        add_groupbox('Make own input (x and y in each line)', VAL_FROMINPUT, layout)
        self.populate_groupbox(VAL_FROMINPUT)
        self.groupboxes[VAL_FROMRAND].setChecked(True)

        button = QPushButton('Run', self)
        button.clicked[bool].connect(self.on_button_pressed)
        layout.addWidget(button)

        self.setCentralWidget(widget)

    def populate_groupbox(self, value):
        gbox = self.groupboxes[value]
        layout = QHBoxLayout()
        widgets = []

        if value == VAL_FROMRAND:
            def on_slider_value_changed(value):
                slider = self.sender()
                slider.label.setText('N: %d' % value)

            slider_n = QSlider(Qt.Horizontal, self)
            slider_n.valueChanged[int].connect(on_slider_value_changed)
            label_n = QLabel('', self)
            slider_n.label = label_n
            slider_n.setMinimum(2)
            slider_n.setMaximum(1000)
            slider_n.setValue(DEF_N)
            widgets.append(slider_n)
            widgets.append(label_n)

        elif value == VAL_FROMINPUT:
            textbox = QTextEdit()
            widgets.append(textbox)

        for widget in widgets:
            layout.addWidget(widget)
            gbox.children.append(widget)
        gbox.setLayout(layout)

    def on_button_pressed(self):
        points = []
        gbox = self.groupboxes[self.cur_mode]
        if self.cur_mode == VAL_FROMRAND:
            points = np.random.rand(gbox.children[0].value(), 2)
        elif self.cur_mode == VAL_FROMINPUT:
            text = gbox.children[0].toPlainText()
            for line in text.split('\n'):
                points.append(tuple(map(float, line.split())))
        points = np.array(points)
        points = np.reshape(points, (len(points), 2))
        print(points)
        Solver(points).make_circle()


class Solver:
    def __init__(self, points):
        self.points = points

    def make_circle(self):
        shuffled = [(float(x), float(y)) for (x, y) in self.points]
        random.shuffle(shuffled)

        c = None
        for (i, p) in enumerate(shuffled):
            if c is None or not self.is_in_circle(c, p):
                c = self._make_circle_one_point(shuffled[: i + 1], p)

        x, y, r = c
        plt.plot(self.points[:, 0], self.points[:, 1], 'o')
        plt.plot(x, y, 'o')

        circle = plt.Circle((x, y), r, fill=False)

        ax = plt.gca()
        ax.axis('equal')
        ax.add_artist(circle)
        ax.set_ylim([-.5, 1.5])
        ax.set_xlim([-.5, 1.5])
        plt.show()

    def _make_circle_one_point(self, points, p):
        c = (p[0], p[1], 0.0)
        for (i, q) in enumerate(points):
            if not self.is_in_circle(c, q):
                if c[2] == 0.0:
                    c = self.make_diameter(p, q)
                else:
                    c = self._make_circle_two_points(points[: i + 1], p, q)
        return c

    def _make_circle_two_points(self, points, p, q):
        circ = self.make_diameter(p, q)
        left = None
        right = None
        px, py = p
        qx, qy = q

        for r in points:
            if self.is_in_circle(circ, r):
                continue

            cross = self._cross_product(px, py, qx, qy, r[0], r[1])
            c = self.make_circumcircle(p, q, r)
            if c is None:
                continue
            elif cross > 0.0 and (
                    left is None or self._cross_product(px, py, qx, qy, c[0], c[1]) >
                    self._cross_product(px, py, qx, qy, left[0], left[1])
            ):
                left = c
            elif cross < 0.0 and (
                    right is None or self._cross_product(px, py, qx, qy, c[0], c[1]) <
                    self._cross_product(px, py, qx, qy, right[0], right[1])
            ):
                right = c

        if left is None and right is None:
            return circ
        elif left is None:
            return right
        elif right is None:
            return left
        else:
            return left if (left[2] <= right[2]) else right

    @staticmethod
    def make_circumcircle(p0, p1, p2):
        ax, ay = p0
        bx, by = p1
        cx, cy = p2
        ox = (min(ax, bx, cx) + max(ax, bx, cx)) / 2.0
        oy = (min(ay, by, cy) + max(ay, by, cy)) / 2.0
        ax -= ox
        ay -= oy
        bx -= ox
        by -= oy
        cx -= ox
        cy -= oy
        d = (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by)) * 2.0
        if d == 0.0:
            return None
        x = ox + ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (
                    ay - by)) / d
        y = oy + ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (
                    bx - ax)) / d
        ra = math.hypot(x - p0[0], y - p0[1])
        rb = math.hypot(x - p1[0], y - p1[1])
        rc = math.hypot(x - p2[0], y - p2[1])
        return x, y, max(ra, rb, rc)

    @staticmethod
    def make_diameter(p0, p1):
        cx = (p0[0] + p1[0]) / 2.0
        cy = (p0[1] + p1[1]) / 2.0
        r0 = math.hypot(cx - p0[0], cy - p0[1])
        r1 = math.hypot(cx - p1[0], cy - p1[1])
        return cx, cy, max(r0, r1)

    _MULTIPLICATIVE_EPSILON = 1 + 1e-14

    def is_in_circle(self, c, p):
        return c is not None and math.hypot(p[0] - c[0], p[1] - c[1]) <= c[2] * self._MULTIPLICATIVE_EPSILON

    @staticmethod
    def _cross_product(x0, y0, x1, y1, x2, y2):
        return (x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
