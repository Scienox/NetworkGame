from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QStackedWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)

        self.setWindowTitle("Network tools")

        self.setCentralWidget(QWidget(parent=self))

        self.myStyleSheet()

        self.__buildCentralWidget()

        self.__menuBar()

    def __buildCentralWidget(self):
        self.layoutCentralWidget = QVBoxLayout(self.centralWidget())
        self.homeButton = QPushButton(text="<-", parent=self.centralWidget())

        self.stackedWidget = QStackedWidget(parent=self.centralWidget())
        self.homeButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.welcomePage = QWidget(parent=self.stackedWidget)
        self.IpConfigPage = QWidget(parent=self.stackedWidget)
        self.__buildWelcomePage()

        self.stackedWidget.addWidget(self.welcomePage)
        self.stackedWidget.addWidget(self.IpConfigPage)

        self.layoutCentralWidget.addWidget(self.homeButton)
        self.layoutCentralWidget.addStretch(1)
        self.layoutCentralWidget.addWidget(self.stackedWidget)
        self.layoutCentralWidget.addStretch(30)


        """self.layoutCentralWidget = QHBoxLayout(self.centralWidget())
        self.layoutCentralWidget.setParent(self.centralWidget())
        self.widgetIp = QWidget(self.centralWidget())
        self.layoutCentralWidget.addWidget(self.widgetIp)
        self.__buildWidgetiP()"""

    def __buildWelcomePage(self):
        self.layoutWelcomePageGrid = QGridLayout(self.welcomePage)
        self.buttonPageIpconfig = QPushButton(parent=self.welcomePage, text="IpConfig")
        self.buttonPageIpconfig.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.buttonPageBinaryinfo = QPushButton(parent=self.welcomePage, text="Ip binaire")
        self.buttonPageVlsm = QPushButton(parent=self.welcomePage, text="VLSM")

        self.layoutWelcomePageGrid.addWidget(self.buttonPageIpconfig, 0, 0)
        self.layoutWelcomePageGrid.addWidget(self.buttonPageBinaryinfo, 0, 1)
        self.layoutWelcomePageGrid.addWidget(self.buttonPageVlsm, 1, 0, 1, 2)

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

    def myStyleSheet(self):
        stylesheet = """
            * {
                background-color: #21252c;
                color: #acacac;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QWidget {
                
            }
            QPushButton {
                
            }
            QPushButton:hover {
                
            }
            QLabel {
                
            }
            """
        self.setStyleSheet(stylesheet)
