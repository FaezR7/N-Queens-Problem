from copy import deepcopy
import sys
from matplot_utils import FigCanvas, resource_path

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow, QPushButton,
                             QHBoxLayout, QVBoxLayout, QWidget,
                             QLabel, QSpinBox, QListWidget)
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
# import turtle


class NQueensProblem:
    def __init__(self) -> None:
        self.view = NQueensProblemView()
        self.connect_buttons()

        # print(f'possible solutions: {len(self.possible_solutions)}\n')
        # for solution in self.possible_solutions:
        #     print_matrix(solution, self.n)
        #     print()
        pass

    def connect_buttons(self) -> None:
        self.view.run_btn.clicked.connect(self.add_soltions_to_list)
        self.view.solutions_list.currentRowChanged.connect(
            self.show_current_solution
            )

    def add_soltions_to_list(self) -> None:
        self.n = self.view.n_spinbox.value()
        self.possible_solutions = []
        board = [[0 for i in range(self.n)] for i in range(self.n)]
        self.nQueens(board)
        solutions_count = len(self.possible_solutions)
        self.view.solutions_count_label.setText(f'All solutions count: {solutions_count}')

        self.view.solutions_list.clear()
        self.view.solutions_list.addItems(
            [f'Solution {i}' for i in range(1, solutions_count + 1)]
            )

    def show_current_solution(self, row: int) -> None:
        if row in range(len(self.possible_solutions)):
            current_solution = self.possible_solutions[row]
        else:
            current_solution = []
        # print_matrix(current_solution, self.n)
        draw_solution(self.n, self.view.canvas, current_solution)
        self.view.canvas.draw()

    def nQueens(self, board: list, col: int = 0):
        if col == self.n:
            _board = deepcopy(board)
            self.possible_solutions.append(_board)
            return True

        res = False
        for row in range(self.n):
            if self.is_safe(board, row, col):
                board[row][col] = 1

                # if nQueens(board, col + 1):
                #     return True
                res = self.nQueens(board, col + 1) or res

                board[row][col] = 0

        return res

    def is_safe(self, board: list, row: int, col: int) -> bool:
        # check the validity of the current row possible choices
        for i in range(col):
            if board[row][i] == 1:
                return False

        r = row
        c = col
        # check the upper diagonal validity
        while r >= 0 and c >= 0:
            if board[r][c] == 1:
                return False
            r -= 1
            c -= 1

        r = row
        c = col
        # check the lower diagonal validity
        while r < self.n and c >= 0:
            if board[r][c] == 1:
                return False
            r += 1
            c -= 1

        # return True if the current row and col is a valid placement
        return True

    def show(self):
        self.view.main_window.show()


class NQueensProblemView:
    def __init__(self) -> None:
        self.logo = resource_path('crown.png')
        self.main_window = QMainWindow()
        self.main_window.setWindowTitle('N Queens Problem')
        self.main_window.resize(1000, 700)
        self.main_window.setWindowIcon(QIcon(self.logo))
        self.central()

    def central(self) -> None:
        # main layout
        hbox = QHBoxLayout()

        # 1st column (for input(s) and solutions list)
        vbox = QVBoxLayout()

        logo = self.logo_box()
        vbox.addLayout(logo)

        inputs = self.inputs()
        vbox.addLayout(inputs)

        solutions_list_box = self.solutions_list_box()
        vbox.addLayout(solutions_list_box)

        close_btn = QPushButton('Close')
        close_btn.clicked.connect(sys.exit)
        vbox.addWidget(close_btn)

        hbox.addLayout(vbox)

        preview_box = self.preview_box()
        hbox.addLayout(preview_box, 2)

        central_widget = QWidget()
        central_widget.setLayout(hbox)

        self.main_window.setCentralWidget(central_widget)

    def logo_box(self) -> QHBoxLayout:
        # main layout
        hbox = QHBoxLayout()

        icon = QLabel()
        icon.setStyleSheet(f'border-image: url({self.logo});')
        icon.setFixedSize(80, 80)
        hbox.addWidget(icon)

        return hbox

    def inputs(self) -> QHBoxLayout:
        hbox = QHBoxLayout()

        n_label = QLabel('Number of queens (n):')
        hbox.addWidget(n_label)

        self.n_spinbox = QSpinBox()
        self.n_spinbox.setValue(8)
        self.n_spinbox.setMinimum(1)
        self.n_spinbox.setMaximum(12)
        hbox.addWidget(self.n_spinbox)

        hbox.addStretch(1)

        self.run_btn = QPushButton('Run!')
        self.run_btn.resize(80, 50)
        hbox.addWidget(self.run_btn)

        hbox.addStretch(4)

        return hbox

    def solutions_list_box(self) -> QVBoxLayout:
        # main layout
        vbox = QVBoxLayout()

        self.solutions_list = QListWidget()
        self.solutions_list.setSelectionMode(1)
        vbox.addWidget(self.solutions_list)

        self.solutions_count_label = QLabel()
        vbox.addWidget(self.solutions_count_label)

        return vbox

    def preview_box(self) -> QVBoxLayout:
        # main layout
        vbox = QVBoxLayout()

        self.canvas = FigCanvas()
        vbox.addWidget(self.canvas)

        return vbox


def print_matrix(board: list, n: int) -> None:
    for row in range(n):
        print()
        for col in range(n):
            print(board[row][col], end=' ')

    print()


def draw_solution(n: int, canvas: FigCanvas, current_solution: list) -> None:

    plot: plt = canvas.plt
    ax: Axes = canvas.axes
    plot.close()
    # fig = canvas.fig
    ax.clear()

    color = 'white'
    for j in range(n):
        for i in range(n):
            center = (i, -j)
            if i == 0:
                if j == 0:
                    first_row_color = color
                else:
                    color = 'black' if first_row_color == 'white' else 'white'
                    first_row_color = color
            else:
                color = 'black' if color == 'white' else 'white'
            anchor_point = (center[0] - 0.5, center[1] + 0.5)
            square = plot.Rectangle(anchor_point, 1, -1, linewidth=0, fc=color)
            ax.add_patch(square)
            # print(square.get_bbox())

            if current_solution and current_solution[j][i] == 1:
                ax.text(center[0], center[1], '♛', fontsize=round(300 / n), ha='center',
                        va='center', color='black' if color == 'white' else 'white')

    ax.axis('equal')
    ax.axis('off')
