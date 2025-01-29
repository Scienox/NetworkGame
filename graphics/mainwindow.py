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
        layoutleft = QVBoxLayout(left)
        left.setLayout(layoutleft)
        self.layoutWidgetIp.addStretch(1)
        self.layoutWidgetIp.addWidget(left)
        #self.layoutWidgetIp.addStretch(1)

        self.pushButtonIp = QPushButton(parent=left, text="Generate")
        self.lineEditIp = QLineEdit(parent=left)
        layoutleft.addStretch(1)
        layoutleft.addWidget(self.lineEditIp)
        layoutleft.addWidget(self.pushButtonIp)
        #layoutleft.addStretch(1)

    def __menuBar(self):
        pass

