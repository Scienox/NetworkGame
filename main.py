import sys
from graphics.mainwindow import MainWindow
from PySide6.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    mainWindow = MainWindow()

    mainWindow.show()
    sys.exit(app.exec())

