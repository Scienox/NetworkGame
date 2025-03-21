from PySide6.QtWidgets import (QLabel, QLineEdit, QPushButton, QDialog, QComboBox, QFormLayout, QSpinBox, QHBoxLayout)
from PySide6.QtCore import (QThread, Signal, QEventLoop)
from time import sleep
from ip_untils.ip_edit import IpEdit
from ip_untils.ip import IP
from random import randint, choice
from types import FunctionType
from .custom_widget import CustomQSpinBox


class GameThreadIpAnalyse(QThread):
    validateSignal = Signal(list)
    selectChallSignal = Signal()
    playSignal = Signal()

    def __init__(self, parent, timer:QLabel, randomIp:QLabel,
                 randomCidr:QLabel, buttonValidate:QPushButton, inputs:list):
        super().__init__(parent)
        self._buttonValidate = buttonValidate
        self._buttonValidate.clicked.connect(self.validate)
        self._isRunning = False
        self.timer = timer
        self._minutes = 0
        self._secondes = -1
        self._randomIp = randomIp
        self._randomCidr = randomCidr
        self._inputs = inputs
        self.selectChallSignal.connect(self.selectChallMessage)
        self._timeOut = (60, 0)
        self.ipEdit:IpEdit
        self.accept = True

    def __bool__(self):
        return self.isRunning

    @property
    def secondes(self):
        return self._secondes
    
    @property
    def minutes(self):
        return self._minutes
    
    @property
    def _addMinute(self):
        self._minutes += 1
        self._resetSecondes
        if self._minutes == 60:
            self.stop()

    @property
    def _addSeconde(self):
        self._secondes += 1
        if  60 == self._secondes:
            self._addMinute

    @property
    def _resetSecondes(self):
        self._secondes = 0

    @property
    def isRunning(self):
        return self._isRunning

    def stop(self):
        self._isRunning = False
        self._buttonValidate.setEnabled(False)
        [element.setEnabled(False) for element in self._inputs]
        self._setIpEdit
        self._setIpEdit == self.ip
        print(self.ipEdit.show_display)

    def reset(self):
        self._minutes = 0
        self._secondes = -1
        [self.translationDetect(element.setText('') if isinstance(element, QLineEdit) else element.setCurrentIndex(0)) for element in self._inputs]
        [element.setEnabled(True) for element in self._inputs]
        self._isRunning = True

    def run(self):
        self.selectChallSignal.emit()
        loop = QEventLoop(self)
        self.validateSignal.connect(lambda options: self.generateChallenge(loop, options))
        loop.exec()
        if self.accept:
            self.reset()
            self._buttonValidate.setEnabled(True)
            self.play()

    def play(self):
        while self.isRunning:
            self._addSeconde
            timer = self._minutes, self._secondes
            self.timer.setText(f"{timer[0]:02}:{timer[1]:02}")
            if self.isTimeOut():
                self.stop()
            sleep(1)

    def translationDetect(self, element):
        reservation = ["Privée", "Publique", "LocalHost", "Multicast"]
        if element in reservation:
            if element == reservation[0]:
                return "private"
            elif element == reservation[1]:
                return "public"
            elif element == reservation[2]:
                return "localhost"
            elif element == reservation[3]:
                return "multicast"
        elif element == "@réseau":
            return "@network"
        elif element == '':
            return 'None'
        else:
            return element

    def generateChallenge(self, loop, options):
        self.accept = True
        if len(options) != 0:
            class_, reservation, type_, cidr, time = options

            self.setTimeOut(time)
            randomByte = [randint(0, 255) for _ in range(4)]
            if type == "!random" and class_ == "!random" and reservation == "!random":
                randomByte = []
            elif class_ == "A":
                randomByte[0] = f"{randint(0, 126)}"
                if reservation == "Privée":
                    randomByte[0] = "10"
                elif reservation == "Publique":
                    beforePrivate = randint(0, 9)
                    afterPrivate = randint(11, 126)
                    randomByte[0] = choice([beforePrivate, afterPrivate])

            randomIp = ".".join(f"{byte}" for byte in randomByte)
            randomCidr = randint(0, 30)
            self.ip = IP(randomIp, randomCidr)

            self._randomIp.setText(self.ip.ipHost)
            self._randomCidr.setText('/' + str(self.ip.cidr))
        else:
            self.accept = False

        loop.quit()

    def selectChallMessage(self):
        options = selectChallengeAnalyseIp(self.parent())
        self.validateSignal.emit(options.choices if options else [])

    def validate(self):
        self.stop()
 
    def setTimeOut(self, time):
        self._timeOut = time
    
    def isTimeOut(self):
        return self.getTimer == self._timeOut

    @property
    def getTimer(self):
        return self._minutes, self._secondes

    @property
    def _setIpEdit(self):
        inputs = self._inputs
        ipEditList = [self.translationDetect(element.text() if isinstance(element, QLineEdit) else element.currentText()) for element in inputs]
        ipEdit = IpEdit(
            *ipEditList
        )
        self.ipEdit = ipEdit
        self.ipEdit == self.ip


class selectChallengeAnalyseIp(QDialog):
    def __init__(self, window):
        super().__init__(parent=window)
        self.validated = False
        self.choices:list

        MainLayout = QFormLayout(self)
        random = "Aléatoire"

        self.comboBoxClass = QComboBox(self)
        self.comboBoxClass.addItems([random, "A", "B", "C", "D", "E"])

        self.comboBoxReservation = QComboBox(self)
        self.comboBoxReservation.addItems([random, "Privée", "Publique", "LocalHost", "Multicast", "IETF"])

        self.comboBoxType = QComboBox(self)
        self.comboBoxType.addItems([random, "@Réseau", "@Broadcast", "@Ip"])

        self.spinBoxCidr = QSpinBox(self)
        self.spinBoxCidr.setMinimum(1)
        self.spinBoxCidr.setMaximum(30)

        layoutTime = QHBoxLayout(self)
        self.spinBoxTimeMin = CustomQSpinBox(self)
        self.spinBoxTimeMin.setMinimum(2)
        self.spinBoxTimeMin.setMaximum(60)
        self.spinBoxTimeMin.setValue(60)
        self.spinBoxTimeSec = CustomQSpinBox(self)
        self.spinBoxTimeSec.setMaximum(59)
        layoutTime.addWidget(self.spinBoxTimeMin)
        layoutTime.addWidget(QLabel("min"))
        layoutTime.addWidget(self.spinBoxTimeSec)
        layoutTime.addWidget(QLabel("s"))

        layoutClose = QHBoxLayout(self)
        validateButton = QPushButton("Valider")
        validateButton.clicked.connect(self.validate_choices)
        cancelButton = QPushButton("Annuler")
        cancelButton.clicked.connect(self.accept)
        layoutClose.addWidget(validateButton)
        layoutClose.addWidget(cancelButton)

        MainLayout.addRow("Classe:", self.comboBoxClass)
        MainLayout.addRow("Réservation:", self.comboBoxReservation)
        MainLayout.addRow("Type:", self.comboBoxType)
        MainLayout.addRow("CIDR:", self.spinBoxCidr)
        MainLayout.addRow("Temps:", layoutTime)
        MainLayout.addRow(layoutClose)

        self.setLayout(MainLayout)

        self.exec()

    def __bool__(self):
        return self.validated

    def setValidated(self):
        self.validated = True

    def validate_choices(self):
        choiceClass = self.comboBoxClass.currentIndex()
        choiceReservation = self.comboBoxReservation.currentIndex()
        choiceType = self.comboBoxType.currentIndex()
        choiceCidr = self.spinBoxCidr.value()
        choiceTime = self.spinBoxTimeMin.value(), self.spinBoxTimeSec.value()
        self.accept()
        self.choices = [choiceClass, choiceReservation, choiceType, choiceCidr, choiceTime]
        self.setValidated()

