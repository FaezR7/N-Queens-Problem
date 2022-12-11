import sys
from PyQt5.QtWidgets import QApplication
from n_queens_problem import NQueensProblem


if __name__ == '__main__':
    app = QApplication(sys.argv)
    n_queens = NQueensProblem()
    n_queens.show()
    sys.exit(app.exec_())