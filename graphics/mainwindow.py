from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)

        self.setWindowTitle("Network tools")

        self.setCentralWidget(QWidget(parent=self))

        self.__buildCentralWidget()

        self.__menuBar()

    def __buildCentralWidget(self):
        self.layoutCentralWidget = QHBoxLayout(self.centralWidget())
        self.layoutCentralWidget.setParent(self.centralWidget())
        self.widgetIp = QWidget(self.centralWidget())
        self.layoutCentralWidget.addWidget(self.widgetIp)
        self.__buildWidgetiP()

    def __buildWidgetiP(self):
        self.layoutWidgetIp = QHBoxLayout(self.widgetIp)
        self.widgetIp.setLayout(self.layoutWidgetIp)
        left = QWidget(parent=self.widgetIp)
        right = QWidget(parent=self.widgetIp)
        layoutLeft = QVBoxLayout(left)
        layoutRight = QVBoxLayout(right)
        left.setLayout(layoutLeft)
        right.setLayout(layoutRight)
        self.layoutWidgetIp.addWidget(left)
        self.layoutWidgetIp.addWidget(right)

        self.pushButtonIp = QPushButton(parent=left, text="Generate")
        self.lineEditIp = QLineEdit(parent=left)
        layoutLeft.addWidget(self.lineEditIp)
        layoutLeft.addWidget(self.pushButtonIp)
        layoutLeft.addStretch(1)

        self.lineEditCidr = QLineEdit(parent=right)
        layoutRight.addWidget(self.lineEditCidr)
        layoutRight.addStretch(1)

    def __menuBar(self):
        pass

