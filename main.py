import sys
from graphics.mainwindow import MainWindow
from PySide6.QtWidgets import QApplication
from graphics.connect import printIp


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()

    mainWindow.pushButtonIp.clicked.connect(lambda _: printIp(mainWindow.lineEditIp.text()))

    mainWindow.show()
    sys.exit(app.exec())

