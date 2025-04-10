from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout,
                                QVBoxLayout, QGridLayout, QPushButton,
                                QLineEdit, QStackedWidget, QTableWidget,
                                QComboBox, QHeaderView, QLabel, QSpacerItem,
                                QSizePolicy, QFormLayout
                                )
from PySide6.QtCore import Qt
from .connect import *
from .game import GameThreadIpAnalyse


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)

        self.setMinimumSize(720, 600)
        self.setWindowTitle("Network tools")
        self.comboBoxCidr = ["CIDR", "Masque de sous réseau", "Nombre d'utilisateur"]

        self.setCentralWidget(QWidget(parent=self))

        self.myStyleSheet()

        self.__buildCentralWidget()

        self.__menuBar()

    def __buildCentralWidget(self):
        self.layoutCentralWidget = QVBoxLayout(self.centralWidget())
        self.homeButton = QPushButton(text="<-", parent=self.centralWidget())

        self.spacerForTable = QSpacerItem(25, 25, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.stackedWidget = QStackedWidget(parent=self.centralWidget())
        self.homeButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.welcomePage = QWidget(parent=self.stackedWidget)
        self.IpConfigPage = QWidget(parent=self.stackedWidget)
        self.ipBinaryPage = QWidget(parent=self.stackedWidget)
        self.vlsmPage = QWidget(parent=self.stackedWidget)
        self.addressingPlanPage = QWidget(parent=self.stackedWidget)
        self.trainingGamePage = QWidget(parent=self.stackedWidget)
        self.__buildWelcomePage()

        self.stackedWidget.addWidget(self.welcomePage)
        self.stackedWidget.addWidget(self.IpConfigPage)
        self.stackedWidget.addWidget(self.ipBinaryPage)
        self.stackedWidget.addWidget(self.vlsmPage)
        self.stackedWidget.addWidget(self.addressingPlanPage)
        self.stackedWidget.addWidget(self.trainingGamePage)

        self.layoutCentralWidget.addWidget(self.homeButton)
        self.layoutCentralWidget.addWidget(self.stackedWidget)

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
        self.buttonPageTrainingGame = QPushButton(parent=self.stackedWidget, text="Jeu d'entrainement")
        self.buttonPageTrainingGame.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))

        self.layoutWelcomePageGrid.addWidget(self.buttonPageIpconfig, 0, 0)
        self.layoutWelcomePageGrid.addWidget(self.buttonPageBinary, 0, 1)
        self.layoutWelcomePageGrid.addWidget(self.buttonPageVlsm, 1, 0)
        self.layoutWelcomePageGrid.addWidget(self.buttonPageAddressingPlan, 1, 1)
        self.layoutWelcomePageGrid.addWidget(self.buttonPageTrainingGame, 2, 0, 1, -1)

        self.__buildIpConfig()
        self.__buildIpBinary()
        self.__buildVlsm()
        self.__buildAddressingPlan()
        self.__buildMainGame()

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
        tableNoResizeRow(self.tableIpConfig)

        self.layoutIpConfigWidget.addWidget(self.labelIp, 0, 0, 1, 1)
        self.layoutIpConfigWidget.addWidget(self.lineEditIp, 0, 1, 1, 1)
        self.layoutIpConfigWidget.addWidget(self.comboboxSelectType, 0, 2, 1, 1)
        self.layoutIpConfigWidget.addWidget(self.lineEditNetworkLimite, 0, 3, 1, 1)
        self.layoutIpConfigWidget.addWidget(self.pushButtonIp, 1, 0, 1, -1)
        self.layoutIpConfigWidget.addWidget(self.tableIpConfig, 2, 0, 1, -1)
        self.layoutIpConfigWidget.addItem(self.spacerForTable, 3, 0, 1, -1)

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
        tableNoResizeRow(self.tableIpBinary)

        self.layoutIpBinary.addWidget(self.labelIpB, 0, 0, 1, 1)
        self.layoutIpBinary.addWidget(self.lineEditIpB, 0, 1, 1, 1)
        self.layoutIpBinary.addWidget(self.comboboxSelectTypeB, 0, 2, 1, 1)
        self.layoutIpBinary.addWidget(self.lineEditNetworkLimiteB, 0, 3, 1, 1)
        self.layoutIpBinary.addWidget(self.pushButtonIpB, 1, 0, 1, 4)
        self.layoutIpBinary.addWidget(self.tableIpBinary, 2, 0, 1, 4)
        self.layoutIpBinary.addItem(self.spacerForTable, 3, 0, 1, -1)

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
        updateRowSizeTable(self.tableVlsmNetwork)
        tableNoResizeRow(self.tableVlsmNetwork)
        self.tableVlsmNetwork.setColumnWidth(0, 200)
        updateRowSizeTable(self.tableVlsmNetwork)
        self.tableVlsmNetwork.horizontalHeader().setVisible(False)
        self.tableVlsmNetwork.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableVlsmNetwork.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.pushButtonAddSubNetwork = QPushButton(self.vlsmPage, text="Ajouté un sous réseau")
        self.pushButtonRemoveSubNetwork = QPushButton(self.vlsmPage, text="Supprimé le sous réseau sélectionné")

        columns = [
            "Nom", "Masque de sous réseau", "@Réseau", "Utilisateurs maximum", "CIDR"
        ]
        self.tableVlsm = QTableWidget(0, len(columns), parent=self.vlsmPage)
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
        self.layoutVlsm.addItem(self.spacerForTable, 5, 0, 1, -1)

        self.pushButtonAddSubNetwork.clicked.connect(lambda: addNetwork(self.tableVlsmNetwork))
        self.pushButtonRemoveSubNetwork.clicked.connect(lambda: removeNetwork(self.tableVlsmNetwork))
        self.pushButtonIpV.clicked.connect(lambda: makeVlsm(self.tableVlsmNetwork,
                                                            self.tableVlsm, self.lineEditIpV.text(),
                                                            self.comboboxSelectTypeV.currentIndex(),
                                                            self.lineEditNetworkLimiteV.text()))

    def __buildAddressingPlan(self):
        self.layoutAddressingPLan = QGridLayout(self.addressingPlanPage)
        self.addressingPlanPage.setLayout(self.layoutAddressingPLan)

        self.pushButtonAddBeforeTarget = QPushButton(parent=self.addressingPlanPage, text="Ajouter une ligne avant la ligne sélectionnée")
        self.pushButtonAddAfterTarget = QPushButton(parent=self.addressingPlanPage, text="Ajouter une ligne après la ligne sélectionnée")
        self.pushButtonAddBefore = QPushButton(parent=self.addressingPlanPage, text="Ajouter une ligne au début")
        self.pushButtonAddAfter = QPushButton(parent=self.addressingPlanPage, text="Ajouter une ligne à la fin")
        self.pushButtonRemove = QPushButton(parent=self.addressingPlanPage, text="Supprimer la ligne sélectionnée")

        self.layoutImportVlsm = QGridLayout(parent=self.addressingPlanPage)
        self.labelImportVlsm = QLabel(parent=self.addressingPlanPage, text="Importer depuis")
        self.comboBoxImport = QComboBox(parent=self.addressingPlanPage)
        self.comboBoxImport.addItems(["VLSM", "CSV", "Excel"])
        self.pushButtonImport = QPushButton(parent=self.addressingPlanPage, text="Importer")
        self.pushButtonExport = QPushButton(parent=self.addressingPlanPage, text="Exporter")

        columns = [
            "Appareil", "Nom du réseau", "Interface",
            "@Ip", "Masque de sous réseau", "@Reseau",
            "Vlan", "Passerelle", "@Mac"
        ]
        self.tableAddressingPlan = QTableWidget(0, len(columns))
        self.tableAddressingPlan.setHorizontalHeaderLabels(columns)
        self.tableAddressingPlan.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableAddressingPlan.setColumnWidth(0, 200)
        self.tableAddressingPlan.verticalHeader().setVisible(False)

        self.layoutAddressingPLan.addWidget(self.pushButtonRemove, 0, 0, 1, -1)
        self.layoutAddressingPLan.addWidget(self.pushButtonAddAfter, 1, 0, 1, 1)
        self.layoutAddressingPLan.addWidget(self.pushButtonAddBefore, 1, 1, 1, 1)
        self.layoutAddressingPLan.addWidget(self.pushButtonAddAfterTarget, 2, 0, 1, 1)
        self.layoutAddressingPLan.addWidget(self.pushButtonAddBeforeTarget, 2, 1, 1, 1)
        self.layoutAddressingPLan.addLayout(self.layoutImportVlsm, 3, 0, 1, 1)
        self.layoutAddressingPLan.addWidget(self.pushButtonImport, 3, 1, 1, 1)
        self.layoutAddressingPLan.addWidget(self.tableAddressingPlan, 4, 0, 1, -1)
        self.layoutAddressingPLan.addItem(self.spacerForTable, 5, 0, 1, -1)
        self.layoutAddressingPLan.addWidget(self.pushButtonExport, 6, 0, 1, -1)

        self.layoutImportVlsm.addWidget(self.labelImportVlsm, 0, 0)
        self.layoutImportVlsm.addWidget(self.comboBoxImport, 0, 1)

        self.pushButtonRemove.clicked.connect(lambda: removeRowSelected(self.tableAddressingPlan))
        self.pushButtonAddAfter.clicked.connect(lambda: addAfterRowAddressingPlan(self.tableAddressingPlan))
        self.pushButtonAddBefore.clicked.connect(lambda: addBeforeRowAddressingPlan(self.tableAddressingPlan))
        self.pushButtonAddAfterTarget.clicked.connect(lambda: addAfterTRowAddressingPlan(self.tableAddressingPlan))
        self.pushButtonAddBeforeTarget.clicked.connect(lambda: addBeforeTRowAddrerssingPLan(self.tableAddressingPlan))
        self.pushButtonImport.clicked.connect(lambda: toImport(self.tableAddressingPlan, self.comboBoxImport.currentIndex(), self.tableVlsm))
        self.pushButtonExport.clicked.connect(lambda: toExport(self.tableAddressingPlan, columns))

    def __buildMainGame(self):
        self.layoutTrainingGamePage = QVBoxLayout(self.trainingGamePage)
        self.trainingGamePage.setLayout(self.layoutTrainingGamePage)

        self.buttonReturnGameMenu = QPushButton(parent=self.trainingGamePage, text="<-")
        self.stackedWidgetGame = QStackedWidget(parent=self.trainingGamePage)
        self.widgetIpAnalyse = QWidget(parent=self.stackedWidgetGame)
        self.widgetMenuGame = QWidget(parent=self.stackedWidgetGame)
        self.layoutMenuGame = QGridLayout(self.widgetMenuGame)
        self.widgetMenuGame.setLayout(self.layoutMenuGame)

        self.buttonIpAnalyse = QPushButton(parent=self.widgetMenuGame, text="Analyse Ip")

        self.layoutMenuGame.addWidget(self.buttonIpAnalyse, 0, 0, 1, -1)

        self.stackedWidgetGame.addWidget(self.widgetMenuGame)
        self.stackedWidgetGame.addWidget(self.widgetIpAnalyse)

        self.layoutTrainingGamePage.addWidget(self.buttonReturnGameMenu)
        self.layoutTrainingGamePage.addWidget(self.stackedWidgetGame)

        self.buttonReturnGameMenu.clicked.connect(lambda: self.stackedWidgetGame.setCurrentIndex(0))
        self.buttonIpAnalyse.clicked.connect(lambda: self.stackedWidgetGame.setCurrentIndex(1))

        self.__IpAnalyseScreen()
        
    def __IpAnalyseScreen(self):
        self.layoutIpAnalyse = QGridLayout(self.widgetIpAnalyse)
        self.widgetIpAnalyse.setLayout(self.layoutIpAnalyse)

        self.widgetGameInfo = QWidget(parent=self.widgetIpAnalyse)
        self.layoutGameInfo = QHBoxLayout(self.widgetGameInfo)
        self.widgetGameInfo.setLayout(self.layoutGameInfo)
        self.labelTimer = QLabel(parent=self.widgetGameInfo, text="00:00")
        self.labelRandomIp = QLabel(parent=self.widgetGameInfo, text="_._._._")
        self.labelRandomCidr = QLabel(parent=self.widgetGameInfo, text="/_")
        self.buttonStartAnalyseIp = QPushButton(parent=self.widgetGameInfo, text="Démarrer")
        self.layoutGameInfo.addWidget(self.labelTimer)
        self.layoutGameInfo.addWidget(self.labelRandomIp)
        self.layoutGameInfo.addWidget(self.labelRandomCidr)
        self.layoutGameInfo.addWidget(self.buttonStartAnalyseIp)

        self.widgetAskIpAnalyse = QWidget(parent=self.widgetIpAnalyse)
        self.formLayoutAskIpAnalyse = QFormLayout(self.widgetAskIpAnalyse)
        self.widgetAskIpAnalyse.setLayout(self.formLayoutAskIpAnalyse)
        modelLineEditForm = lambda: QLineEdit(parent=self.widgetAskIpAnalyse)
        modelComboBoxForm = lambda: QComboBox(parent=self.widgetAskIpAnalyse)
        self.comboBoxFormClass = modelComboBoxForm()
        self.comboBoxFormClass.addItems(["", "A", "B", "C", "D", "E"])
        self.comboBoxFormType = modelComboBoxForm()
        self.comboBoxFormType.addItems(["", "@réseau", "@broadcast", "@Ipv4"])
        self.comboBoxFormReservation = modelComboBoxForm()
        self.comboBoxFormReservation.addItems(["", "Privée", "Publique", "LocalHost", "Multicast", "IETF"])
        self.lineEditFormIpv4 = modelLineEditForm()
        self.lineEditFormMask = modelLineEditForm()
        self.lineEditFormNetwork = modelLineEditForm()
        self.lineEditFormAvaibleHosts = modelLineEditForm()
        self.lineEditFormFirstHost = modelLineEditForm()
        self.lineEditFormLastHost = modelLineEditForm()
        self.lineEditFormBroadcast = modelLineEditForm()
        self.lineEditFormNextNetwork = modelLineEditForm()
        self.buttonValidateIpAnalyse = QPushButton(parent=self.widgetAskIpAnalyse, text="Valider")
        self.formLayoutAskIpAnalyse.addRow("Classe:", self.comboBoxFormClass)
        self.formLayoutAskIpAnalyse.addRow("Type:", self.comboBoxFormType)
        self.formLayoutAskIpAnalyse.addRow("Réservation:", self.comboBoxFormReservation)
        self.formLayoutAskIpAnalyse.addRow("@Ipv4:", self.lineEditFormIpv4)
        self.formLayoutAskIpAnalyse.addRow("Masque de sous réseau:", self.lineEditFormMask)
        self.formLayoutAskIpAnalyse.addRow("@Réseau: ", self.lineEditFormNetwork)
        self.formLayoutAskIpAnalyse.addRow("Hôtes disponibles:", self.lineEditFormAvaibleHosts)
        self.formLayoutAskIpAnalyse.addRow("1ère @Disponible:", self.lineEditFormFirstHost)
        self.formLayoutAskIpAnalyse.addRow("Dernière @Disponible:", self.lineEditFormLastHost)
        self.formLayoutAskIpAnalyse.addRow("@Broadcast:", self.lineEditFormBroadcast)
        self.formLayoutAskIpAnalyse.addRow("Réseau suivant:", self.lineEditFormNextNetwork)
        self.formLayoutAskIpAnalyse.addWidget(self.buttonValidateIpAnalyse)

        inputs = [
            self.comboBoxFormClass, self.comboBoxFormType, self.comboBoxFormReservation,
            self.lineEditFormIpv4, self.lineEditFormMask, self.lineEditFormNetwork,
            self.lineEditFormAvaibleHosts, self.lineEditFormFirstHost, self.lineEditFormLastHost,
            self.lineEditFormBroadcast, self.lineEditFormNextNetwork
        ]
        [element.setEnabled(False) for element in inputs]

        self.layoutIpAnalyse.addWidget(self.widgetGameInfo, 0, 0, 1, -1)
        self.layoutIpAnalyse.addWidget(self.widgetAskIpAnalyse, 1, 0, -1, -1)
        self.layoutIpAnalyse.addItem(self.spacerForTable, 2, 0)

        self.timerIpAnalyse = GameThreadIpAnalyse(self.window(), self.labelTimer, self.labelRandomIp,
                                                  self.labelRandomCidr, self.buttonValidateIpAnalyse, inputs)

        self.buttonValidateIpAnalyse.setEnabled(False)
        self.buttonStartAnalyseIp.clicked.connect(lambda: startIpAnalyse(self.timerIpAnalyse))

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
                border: none;
                gridline-color: #1f4141;
                color: black;
                background-color: #898b8b;
                selection-color: #acacac;
                selection-background-color: #2e5f5f;
            }
            QHeaderView {
                border-radius: 0px;
                font-weight: normal;
            }
            QHeaderView:section {
                border-color: #1f4141;
                background-color: #21252c;
            }
            QScrollBar:horizontal {
                background: #898b8b;
                height: 15px;
                border: 2px solid #1f4141;
                border-radius: 0px;
                margin: 0px;
                border-bottom-left-radius: 5px;
                border-bottom-right-radius: 5px;
            }
            QScrollBar:add-line:horizontal, QScrollBar:sub-line:horizontal {
                width: 0px;
                height: 0px;
            }
            QScrollBar:handle:horizontal {
                background-color: #21252c;
            }
            QScrollBar:handle:horizontal:hover {
                background-color: #2e333d;
            }
            QComboBox {
                combobox-popup: 0;
            }            
            QComboBox QListView {
                border: 2px solid #1f4141;
            }
            QComboBox:down-arrow {
                image: url(graphics/icons/down-arrow.png);
                width: 16px;
                height: 16px;
            }
            QComboBox:drop-down {
                border: none;
            }
            QComboBox QListView:item {
                border: 1px ridge #1f4141;
                border-radius: 0px;
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


    def resizeEvent(self, event):
        updateRowSizeTable(self.tableIpConfig)
        updateRowSizeTable(self.tableIpBinary)
        updateRowSizeTable(self.tableAddressingPlan)
        #updateRowSizeTable(self.tableVlsmNetwork)
        updateRowSizeTable(self.tableVlsm)
        return super().resizeEvent(event)
