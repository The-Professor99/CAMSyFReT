import sys
from PyQt5.QtWidgets import QApplication
from .startApp import LoginUI


def main():
    app = QApplication(sys.argv)
    mainwindow = LoginUI()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
