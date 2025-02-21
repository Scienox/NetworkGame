from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout,
                                QVBoxLayout, QGridLayout, QPushButton,
                                QLineEdit, QStackedWidget, QTableWidget,
                                QComboBox, QHeaderView, QLabel
                                )
from PySide6.QtCore import Qt
from .connect import *


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
        self.ipBinaryPage = QWidget(parent=self.stackedWidget)
        self.vlsmPage = QWidget(parent=self.stackedWidget)
        self.addresingPlanPage = QWidget(parent=self.stackedWidget)
        self.__buildWelcomePage()

        self.stackedWidget.addWidget(self.welcomePage)
        self.stackedWidget.addWidget(self.IpConfigPage)
        self.stackedWidget.addWidget(self.ipBinaryPage)
        self.stackedWidget.addWidget(self.vlsmPage)
        self.stackedWidget.addWidget(self.addresingPlanPage)

        self.layoutCentralWidget.addWidget(self.homeButton)
        #self.layoutCentralWidget.addStretch(1)
        self.layoutCentralWidget.addWidget(self.stackedWidget)
        #self.layoutCentralWidget.addStretch(30)

    def __buildWelcomePage(self):
        self.layoutWelcomePageGrid = QGridLayout(self.welcomePage)
        self.buttonPageIpconfig = QPushButton(parent=self.welcomePage, text="IpConfig")
        self.buttonPageIpconfig.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.buttonPageBinary = QPushButton(parent=self.welcomePage, text="Ip binaire")
        self.buttonPageBinary.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.buttonPageVlsm = QPushButton(parent=self.welcomePage, text="VLSM")
        self.buttonPageVlsm.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.buttonPageAddressingPlan = QPushButton(self.stackedWidget, text="Plan d'adressage")
        self.buttonPageAddressingPlan.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))

        self.layoutWelcomePageGrid.addWidget(self.buttonPageIpconfig, 0, 0)
        self.layoutWelcomePageGrid.addWidget(self.buttonPageBinary, 0, 1)
        self.layoutWelcomePageGrid.addWidget(self.buttonPageVlsm, 1, 0)
        self.layoutWelcomePageGrid.addWidget(self.buttonPageAddressingPlan, 1, 1)

        self.__buildIpConfig()
        self.__buildIpBinary()
        self.__buildVlsm()
        self.__buildAddressingPlan()

    def __buildIpConfig(self):
        self.layoutIpConfigWidget = QGridLayout(self.IpConfigPage)
        self.IpConfigPage.setLayout(self.layoutIpConfigWidget)

        self.labelIp = QLabel(parent=self.IpConfigPage, text="@Ip:")
        self.lineEditIp = QLineEdit(parent=self.IpConfigPage)
        self.comboboxSelectType = QComboBox(parent=self.IpConfigPage)
        self.comboboxSelectType.addItems(["CIDR", "Masque de sous réseau", "Nombre d'utilisateur"])
        self.lineEditNetworkLimite = QLineEdit(parent=self.IpConfigPage)
        self.pushButtonIp = QPushButton(parent=self.IpConfigPage, text="Analyser")
        rows = [
            "Type", "Classe", "Réservation",
            "@Reseau", "Masque de sous réseau", "CIDR",
            "@Ipv4", "1ère @Disponible", "Dernière @Disponible",
            "@BroadCast", "Utilisateurs maximum"
        ]
        self.tableIpConfig = QTableWidget(len(rows), 1, parent=self.IpConfigPage)
        self.tableIpConfig.setVerticalHeaderLabels(rows)
        self.tableIpConfig.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableIpConfig.setColumnWidth(0, 200)
        self.tableIpConfig.horizontalHeader().setVisible(False)

        self.layoutIpConfigWidget.addWidget(self.labelIp, 0, 0, 1, 1)
        self.layoutIpConfigWidget.addWidget(self.lineEditIp, 0, 1, 1, 1)
        self.layoutIpConfigWidget.addWidget(self.comboboxSelectType, 0, 2, 1, 1)
        self.layoutIpConfigWidget.addWidget(self.lineEditNetworkLimite, 0, 3, 1, 1)
        self.layoutIpConfigWidget.addWidget(self.pushButtonIp, 1, 0, 1, 4)
        self.layoutIpConfigWidget.addWidget(self.tableIpConfig, 2, 0, 1, 4)

        self.pushButtonIp.clicked.connect(lambda: showIpConfig(self.lineEditIp.text(), self.comboboxSelectType.currentIndex(),
                                                                self.lineEditNetworkLimite.text(), self.tableIpConfig))

    def __buildIpBinary(self):
        self.layoutIpBinary = QGridLayout(self.ipBinaryPage)
        self.ipBinaryPage.setLayout(self.layoutIpBinary)

        self.labelIpB = QLabel(parent=self.ipBinaryPage, text="@Ip:")
        self.lineEditIpB = QLineEdit(parent=self.ipBinaryPage)
        self.comboboxSelectTypeB = QComboBox(parent=self.ipBinaryPage)
        self.comboboxSelectTypeB.addItems(["CIDR", "Masque de sous réseau", "Nombre d'utilisateur"])
        self.lineEditNetworkLimiteB = QLineEdit(parent=self.ipBinaryPage)
        self.pushButtonIpB = QPushButton(parent=self.ipBinaryPage, text="Analyser")
        rows = [
            "Masque de sous réseau", "@Réseau", "@Ip",
            "1ère @Disponible", "Dernière @Disponible", "@Broadcast"
        ]
        columns = [
            "Format décimal", "Partie binaire du réseau", "Partie binaire d'hôtes"
        ]
        self.tableIpBinary = QTableWidget(len(rows), len(columns), parent=self.ipBinaryPage)
        self.tableIpBinary.setVerticalHeaderLabels(rows)
        self.tableIpBinary.setHorizontalHeaderLabels(columns)
        self.tableIpBinary.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableIpBinary.setColumnWidth(0, 200)

        self.layoutIpBinary.addWidget(self.labelIpB, 0, 0, 1, 1)
        self.layoutIpBinary.addWidget(self.lineEditIpB, 0, 1, 1, 1)
        self.layoutIpBinary.addWidget(self.comboboxSelectTypeB, 0, 2, 1, 1)
        self.layoutIpBinary.addWidget(self.lineEditNetworkLimiteB, 0, 3, 1, 1)
        self.layoutIpBinary.addWidget(self.pushButtonIpB, 1, 0, 1, 4)
        self.layoutIpBinary.addWidget(self.tableIpBinary, 2, 0, 1, 4)

        self.pushButtonIpB.clicked.connect(lambda: showBinaryInfo(self.lineEditIpB.text(), self.comboboxSelectTypeB.currentIndex(),
                                                                  self.lineEditNetworkLimiteB.text(), self.tableIpBinary))

    def __buildVlsm(self):
        self.layoutVlsm = QGridLayout(self.vlsmPage)
        self.vlsmPage.setLayout(self.layoutVlsm)

        self.labelIpV = QLabel(parent=self.vlsmPage, text="@Ip:")
        self.lineEditIpV = QLineEdit(parent=self.vlsmPage)
        self.comboboxSelectTypeV = QComboBox(parent=self.vlsmPage)
        self.comboboxSelectTypeV.addItems(["CIDR", "Masque de sous réseau", "Nombre d'utilisateur"])
        self.lineEditNetworkLimiteV = QLineEdit(parent=self.vlsmPage)
        self.pushButtonIpV = QPushButton(parent=self.vlsmPage, text="Analyser")

        self.tableVlsmNetwork = QTableWidget(2, 0, parent=self.vlsmPage)
        self.tableVlsmNetwork.setVerticalHeaderLabels(["Nom du réseau", "Nombre d'hôtes"])
        self.tableVlsmNetwork.setHorizontalHeaderLabels([])
        #self.tableVlsmNetwork.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableVlsmNetwork.setFixedHeight(
            self.tableVlsmNetwork.rowHeight(0) * self.tableVlsmNetwork.rowCount() + 17
        )
        self.tableVlsmNetwork.setColumnWidth(0, 200)
        self.tableVlsmNetwork.horizontalHeader().setVisible(False)
        self.tableVlsmNetwork.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableVlsmNetwork.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.pushButtonAddSubNetwork = QPushButton(self.vlsmPage, text="Ajouté un sous réseau")
        self.pushButtonRemoveSubNetwork = QPushButton(self.vlsmPage, text="Supprimé le sous réseau sélectionné")

        rows = []
        columns = [
            "Nom", "Masque de sous réseau", "@Réseau", "Utilisateurs maximum", "CIDR"
        ]
        self.tableVlsm = QTableWidget(len(rows), len(columns), parent=self.vlsmPage)
        self.tableVlsm.setVerticalHeaderLabels(rows)
        self.tableVlsm.setHorizontalHeaderLabels(columns)
        self.tableVlsm.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableVlsm.setColumnWidth(0, 200)
        self.tableVlsm.verticalHeader().setVisible(False)

        self.layoutVlsm.addWidget(self.labelIpV, 0, 0, 1, 1)
        self.layoutVlsm.addWidget(self.lineEditIpV, 0, 1, 1, 1)
        self.layoutVlsm.addWidget(self.comboboxSelectTypeV, 0, 2, 1, 1)
        self.layoutVlsm.addWidget(self.lineEditNetworkLimiteV, 0, 3, 1, 1)
        self.layoutVlsm.addWidget(self.tableVlsmNetwork, 1, 0, 1, 4)
        self.layoutVlsm.addWidget(self.pushButtonAddSubNetwork, 2, 0, 1, 2)
        self.layoutVlsm.addWidget(self.pushButtonRemoveSubNetwork, 2, 3, 1, 1)
        self.layoutVlsm.addWidget(self.pushButtonIpV, 3, 0, 1, 4)
        self.layoutVlsm.addWidget(self.tableVlsm, 4, 0, 1, 4)

        self.pushButtonAddSubNetwork.clicked.connect(lambda: addNetwork(self.tableVlsmNetwork))
        self.pushButtonRemoveSubNetwork.clicked.connect(lambda: removeNetwork(self.tableVlsmNetwork))
        self.pushButtonIpV.clicked.connect(lambda: makeVlsm(self.tableVlsmNetwork,
                                                            self.tableVlsm, self.lineEditIpV.text(),
                                                            self.comboboxSelectTypeV.currentIndex(),
                                                            self.lineEditNetworkLimiteV.text()))

    def __buildAddressingPlan(self):
        pass

    def __menuBar(self):
        pass

    def myStyleSheet(self):
        stylesheet = """
            * {
                background-color: #21252c;
                color: #acacac;
                border: 2px solid #1f4141;
                border-radius: 5px;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QTableWidget {
                border: default;
                border-color: default;
            }
            QComboBox {
                
            }
            QComboBox:drop-down {
                border: none;
                
            }
            QComboBox QListView {
                border: none;
                background-color: #2f3f3f;
                margin-top: 0px;
                outline: 0px;
            }
            QComboBox QListView:item {
                border: 5px solid;
                border-radius: 5px;
            }
            QWidget {
                
            }
            QPushButton {
                
            }
            QPushButton:hover {
                
            }
            QLabel {
                border: none;
            }
            """
        self.setStyleSheet(stylesheet)
