from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout,
                                QVBoxLayout, QGridLayout, QPushButton,
                                QLineEdit, QStackedWidget, QTableWidget,
                                QComboBox, QHeaderView, QLabel, QSpacerItem,
                                QSizePolicy, QFormLayout
                                )
from PySide6.QtCore import Qt
from .connect import *
from .game import GameThreadIpv4Analyse


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
        self.Ipv4ConfigPage = QWidget(parent=self.stackedWidget)
        self.ipv4BinaryPage = QWidget(parent=self.stackedWidget)
        self.vlsmPage = QWidget(parent=self.stackedWidget)
        self.addressingPlanPage = QWidget(parent=self.stackedWidget)
        self.trainingGamePage = QWidget(parent=self.stackedWidget)
        self.__buildWelcomePage()

        self.stackedWidget.addWidget(self.welcomePage)
        self.stackedWidget.addWidget(self.Ipv4ConfigPage)
        self.stackedWidget.addWidget(self.ipv4BinaryPage)
        self.stackedWidget.addWidget(self.vlsmPage)
        self.stackedWidget.addWidget(self.addressingPlanPage)
        self.stackedWidget.addWidget(self.trainingGamePage)

        self.layoutCentralWidget.addWidget(self.homeButton)
        self.layoutCentralWidget.addWidget(self.stackedWidget)

    def __buildWelcomePage(self):
        self.layoutWelcomePageGrid = QGridLayout(self.welcomePage)
        self.buttonPageIpv4config = QPushButton(parent=self.welcomePage, text="Ipv4Config")
        self.buttonPageIpv4config.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.buttonPageBinary = QPushButton(parent=self.welcomePage, text="Ipv4 binaire")
        self.buttonPageBinary.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.buttonPageVlsm = QPushButton(parent=self.welcomePage, text="VLSM")
        self.buttonPageVlsm.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.buttonPageAddressingPlan = QPushButton(self.stackedWidget, text="Plan d'adressage")
        self.buttonPageAddressingPlan.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.buttonPageTrainingGame = QPushButton(parent=self.stackedWidget, text="Jeu d'entrainement")
        self.buttonPageTrainingGame.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))

        self.layoutWelcomePageGrid.addWidget(self.buttonPageIpv4config, 0, 0)
        self.layoutWelcomePageGrid.addWidget(self.buttonPageBinary, 0, 1)
        self.layoutWelcomePageGrid.addWidget(self.buttonPageVlsm, 1, 0)
        self.layoutWelcomePageGrid.addWidget(self.buttonPageAddressingPlan, 1, 1)
        self.layoutWelcomePageGrid.addWidget(self.buttonPageTrainingGame, 2, 0, 1, -1)

        self.__buildIpv4Config()
        self.__buildIpv4Binary()
        self.__buildVlsm()
        self.__buildAddressingPlan()
        self.__buildMainGame()

    def __buildIpv4Config(self):
        self.layoutIpv4ConfigWidget = QGridLayout(self.Ipv4ConfigPage)
        self.Ipv4ConfigPage.setLayout(self.layoutIpv4ConfigWidget)

        self.labelIpv4 = QLabel(parent=self.Ipv4ConfigPage, text="@Ipv4:")
        self.lineEditIpv4 = QLineEdit(parent=self.Ipv4ConfigPage)
        self.comboboxSelectType = QComboBox(parent=self.Ipv4ConfigPage)
        self.comboboxSelectType.addItems(["CIDR", "Masque de sous réseau", "Nombre d'utilisateur"])
        self.lineEditNetworkLimite = QLineEdit(parent=self.Ipv4ConfigPage)
        self.pushButtonIpv4 = QPushButton(parent=self.Ipv4ConfigPage, text="Analyser")
        rows = [
            "Type", "Classe", "Réservation",
            "@Reseau", "Masque de sous réseau", "CIDR",
            "@Ipv4", "1ère @Disponible", "Dernière @Disponible",
            "@BroadCast", "Utilisateurs maximum"
        ]
        self.tableIpv4Config = QTableWidget(len(rows), 1, parent=self.Ipv4ConfigPage)
        self.tableIpv4Config.setVerticalHeaderLabels(rows)
        self.tableIpv4Config.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableIpv4Config.setColumnWidth(0, 200)
        self.tableIpv4Config.horizontalHeader().setVisible(False)
        tableNoResizeRow(self.tableIpv4Config)

        self.layoutIpv4ConfigWidget.addWidget(self.labelIpv4, 0, 0, 1, 1)
        self.layoutIpv4ConfigWidget.addWidget(self.lineEditIpv4, 0, 1, 1, 1)
        self.layoutIpv4ConfigWidget.addWidget(self.comboboxSelectType, 0, 2, 1, 1)
        self.layoutIpv4ConfigWidget.addWidget(self.lineEditNetworkLimite, 0, 3, 1, 1)
        self.layoutIpv4ConfigWidget.addWidget(self.pushButtonIpv4, 1, 0, 1, -1)
        self.layoutIpv4ConfigWidget.addWidget(self.tableIpv4Config, 2, 0, 1, -1)
        self.layoutIpv4ConfigWidget.addItem(self.spacerForTable, 3, 0, 1, -1)

        self.pushButtonIpv4.clicked.connect(lambda: showIpv4Config(self.lineEditIpv4.text(), self.comboboxSelectType.currentIndex(),
                                                                self.lineEditNetworkLimite.text(), self.tableIpv4Config))

    def __buildIpv4Binary(self):
        self.layoutIpv4Binary = QGridLayout(self.ipv4BinaryPage)
        self.ipv4BinaryPage.setLayout(self.layoutIpv4Binary)

        self.labelIpv4B = QLabel(parent=self.ipv4BinaryPage, text="@Ipv4:")
        self.lineEditIpv4v = QLineEdit(parent=self.ipv4BinaryPage)
        self.comboboxSelectTypeB = QComboBox(parent=self.ipv4BinaryPage)
        self.comboboxSelectTypeB.addItems(["CIDR", "Masque de sous réseau", "Nombre d'utilisateur"])
        self.lineEditNetworkLimiteB = QLineEdit(parent=self.ipv4BinaryPage)
        self.pushButtonIpv4B = QPushButton(parent=self.ipv4BinaryPage, text="Analyser")
        rows = [
            "Masque de sous réseau", "@Réseau", "@Ipv4",
            "1ère @Disponible", "Dernière @Disponible", "@Broadcast"
        ]
        columns = [
            "Format décimal", "Partie binaire du réseau", "Partie binaire d'hôtes"
        ]
        self.tableIpv4Binary = QTableWidget(len(rows), len(columns), parent=self.ipv4BinaryPage)
        self.tableIpv4Binary.setVerticalHeaderLabels(rows)
        self.tableIpv4Binary.setHorizontalHeaderLabels(columns)
        self.tableIpv4Binary.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableIpv4Binary.setColumnWidth(0, 200)
        tableNoResizeRow(self.tableIpv4Binary)

        self.layoutIpv4Binary.addWidget(self.labelIpv4B, 0, 0, 1, 1)
        self.layoutIpv4Binary.addWidget(self.lineEditIpv4v, 0, 1, 1, 1)
        self.layoutIpv4Binary.addWidget(self.comboboxSelectTypeB, 0, 2, 1, 1)
        self.layoutIpv4Binary.addWidget(self.lineEditNetworkLimiteB, 0, 3, 1, 1)
        self.layoutIpv4Binary.addWidget(self.pushButtonIpv4B, 1, 0, 1, 4)
        self.layoutIpv4Binary.addWidget(self.tableIpv4Binary, 2, 0, 1, 4)
        self.layoutIpv4Binary.addItem(self.spacerForTable, 3, 0, 1, -1)

        self.pushButtonIpv4B.clicked.connect(lambda: showBinaryInfo(self.lineEditIpv4v.text(), self.comboboxSelectTypeB.currentIndex(),
                                                                  self.lineEditNetworkLimiteB.text(), self.tableIpv4Binary))

    def __buildVlsm(self):
        self.layoutVlsm = QGridLayout(self.vlsmPage)
        self.vlsmPage.setLayout(self.layoutVlsm)

        self.labelIpv4V = QLabel(parent=self.vlsmPage, text="@Ipv4:")
        self.lineEditIpv4V = QLineEdit(parent=self.vlsmPage)
        self.comboboxSelectTypeV = QComboBox(parent=self.vlsmPage)
        self.comboboxSelectTypeV.addItems(["CIDR", "Masque de sous réseau", "Nombre d'utilisateur"])
        self.lineEditNetworkLimiteV = QLineEdit(parent=self.vlsmPage)
        self.pushButtonIpv4V = QPushButton(parent=self.vlsmPage, text="Analyser")

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

        self.layoutVlsm.addWidget(self.labelIpv4V, 0, 0, 1, 1)
        self.layoutVlsm.addWidget(self.lineEditIpv4V, 0, 1, 1, 1)
        self.layoutVlsm.addWidget(self.comboboxSelectTypeV, 0, 2, 1, 1)
        self.layoutVlsm.addWidget(self.lineEditNetworkLimiteV, 0, 3, 1, 1)
        self.layoutVlsm.addWidget(self.tableVlsmNetwork, 1, 0, 1, 4)
        self.layoutVlsm.addWidget(self.pushButtonAddSubNetwork, 2, 0, 1, 2)
        self.layoutVlsm.addWidget(self.pushButtonRemoveSubNetwork, 2, 3, 1, 1)
        self.layoutVlsm.addWidget(self.pushButtonIpv4V, 3, 0, 1, 4)
        self.layoutVlsm.addWidget(self.tableVlsm, 4, 0, 1, 4)
        self.layoutVlsm.addItem(self.spacerForTable, 5, 0, 1, -1)

        self.pushButtonAddSubNetwork.clicked.connect(lambda: addNetwork(self.tableVlsmNetwork))
        self.pushButtonRemoveSubNetwork.clicked.connect(lambda: removeNetwork(self.tableVlsmNetwork))
        self.pushButtonIpv4V.clicked.connect(lambda: makeVlsm(self.tableVlsmNetwork,
                                                            self.tableVlsm, self.lineEditIpv4V.text(),
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
            "@Ipv4", "Masque de sous réseau", "@Reseau",
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
        self.widgetIpv4Analyse = QWidget(parent=self.stackedWidgetGame)
        self.widgetMenuGame = QWidget(parent=self.stackedWidgetGame)
        self.layoutMenuGame = QGridLayout(self.widgetMenuGame)
        self.widgetMenuGame.setLayout(self.layoutMenuGame)

        self.buttonIpv4Analyse = QPushButton(parent=self.widgetMenuGame, text="Analyse Ipv4")

        self.layoutMenuGame.addWidget(self.buttonIpv4Analyse, 0, 0, 1, -1)

        self.stackedWidgetGame.addWidget(self.widgetMenuGame)
        self.stackedWidgetGame.addWidget(self.widgetIpv4Analyse)

        self.layoutTrainingGamePage.addWidget(self.buttonReturnGameMenu)
        self.layoutTrainingGamePage.addWidget(self.stackedWidgetGame)

        self.buttonReturnGameMenu.clicked.connect(lambda: self.stackedWidgetGame.setCurrentIndex(0))
        self.buttonIpv4Analyse.clicked.connect(lambda: self.stackedWidgetGame.setCurrentIndex(1))

        self.__Ipv4AnalyseScreen()
        
    def __Ipv4AnalyseScreen(self):
        self.layoutIpv4Analyse = QGridLayout(self.widgetIpv4Analyse)
        self.widgetIpv4Analyse.setLayout(self.layoutIpv4Analyse)

        self.widgetGameInfo = QWidget(parent=self.widgetIpv4Analyse)
        self.layoutGameInfo = QHBoxLayout(self.widgetGameInfo)
        self.widgetGameInfo.setLayout(self.layoutGameInfo)
        self.labelTimer = QLabel(parent=self.widgetGameInfo, text="00:00")
        self.labelRandomIpv4 = QLabel(parent=self.widgetGameInfo, text="_._._._")
        self.labelRandomCidr = QLabel(parent=self.widgetGameInfo, text="/_")
        self.buttonStartAnalyseIpv4 = QPushButton(parent=self.widgetGameInfo, text="Démarrer")
        self.layoutGameInfo.addWidget(self.labelTimer)
        self.layoutGameInfo.addWidget(self.labelRandomIpv4)
        self.layoutGameInfo.addWidget(self.labelRandomCidr)
        self.layoutGameInfo.addWidget(self.buttonStartAnalyseIpv4)

        self.widgetAskIpv4Analyse = QWidget(parent=self.widgetIpv4Analyse)
        self.formLayoutAskIpv4Analyse = QFormLayout(self.widgetAskIpv4Analyse)
        self.widgetAskIpv4Analyse.setLayout(self.formLayoutAskIpv4Analyse)
        modelLineEditForm = lambda: QLineEdit(parent=self.widgetAskIpv4Analyse)
        modelComboBoxForm = lambda: QComboBox(parent=self.widgetAskIpv4Analyse)
        self.comboBoxFormClass = modelComboBoxForm()
        self.comboBoxFormClass.addItems(["", "A", "B", "C", "D", "E"])
        self.comboBoxFormType = modelComboBoxForm()
        self.comboBoxFormType.addItems(["", "@réseau", "@broadcast", "@Ipv4"])
        self.comboBoxFormReservation = modelComboBoxForm()
        self.comboBoxFormReservation.addItems(["", "Privée", "Publique", "LocalHost", "Multicast", "IETF", "APIPA"])
        self.lineEditFormIpv4 = modelLineEditForm()
        self.lineEditFormMask = modelLineEditForm()
        self.lineEditFormNetwork = modelLineEditForm()
        self.lineEditFormAvaibleHosts = modelLineEditForm()
        self.lineEditFormFirstHost = modelLineEditForm()
        self.lineEditFormLastHost = modelLineEditForm()
        self.lineEditFormBroadcast = modelLineEditForm()
        self.lineEditFormNextNetwork = modelLineEditForm()
        self.buttonValidateIpv4Analyse = QPushButton(parent=self.widgetAskIpv4Analyse, text="Valider")
        self.formLayoutAskIpv4Analyse.addRow("Classe:", self.comboBoxFormClass)
        self.formLayoutAskIpv4Analyse.addRow("Type:", self.comboBoxFormType)
        self.formLayoutAskIpv4Analyse.addRow("Réservation:", self.comboBoxFormReservation)
        self.formLayoutAskIpv4Analyse.addRow("@Ipv4:", self.lineEditFormIpv4)
        self.formLayoutAskIpv4Analyse.addRow("Masque de sous réseau:", self.lineEditFormMask)
        self.formLayoutAskIpv4Analyse.addRow("@Réseau: ", self.lineEditFormNetwork)
        self.formLayoutAskIpv4Analyse.addRow("Hôtes disponibles:", self.lineEditFormAvaibleHosts)
        self.formLayoutAskIpv4Analyse.addRow("1ère @Disponible:", self.lineEditFormFirstHost)
        self.formLayoutAskIpv4Analyse.addRow("Dernière @Disponible:", self.lineEditFormLastHost)
        self.formLayoutAskIpv4Analyse.addRow("@Broadcast:", self.lineEditFormBroadcast)
        self.formLayoutAskIpv4Analyse.addRow("Réseau suivant:", self.lineEditFormNextNetwork)
        self.formLayoutAskIpv4Analyse.addWidget(self.buttonValidateIpv4Analyse)

        inputs = [
            self.comboBoxFormClass, self.comboBoxFormType, self.comboBoxFormReservation,
            self.lineEditFormIpv4, self.lineEditFormMask, self.lineEditFormNetwork,
            self.lineEditFormAvaibleHosts, self.lineEditFormFirstHost, self.lineEditFormLastHost,
            self.lineEditFormBroadcast, self.lineEditFormNextNetwork
        ]
        [element.setEnabled(False) for element in inputs]

        self.layoutIpv4Analyse.addWidget(self.widgetGameInfo, 0, 0, 1, -1)
        self.layoutIpv4Analyse.addWidget(self.widgetAskIpv4Analyse, 1, 0, -1, -1)
        self.layoutIpv4Analyse.addItem(self.spacerForTable, 2, 0)

        self.timerIpv4Analyse = GameThreadIpv4Analyse(self.window(), self.labelTimer, self.labelRandomIpv4,
                                                  self.labelRandomCidr, self.buttonValidateIpv4Analyse, inputs)

        self.buttonValidateIpv4Analyse.setEnabled(False)
        self.buttonStartAnalyseIpv4.clicked.connect(lambda: startIpv4Analyse(self.timerIpv4Analyse))

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
        updateRowSizeTable(self.tableIpv4Config)
        updateRowSizeTable(self.tableIpv4Binary)
        updateRowSizeTable(self.tableAddressingPlan)
        #updateRowSizeTable(self.tableVlsmNetwork)
        updateRowSizeTable(self.tableVlsm)
        return super().resizeEvent(event)
