from PySide6.QtWidgets import (QLabel, QLineEdit, QPushButton, QDialog, QComboBox, QFormLayout, QSpinBox, QHBoxLayout)
from PySide6.QtCore import (QThread, Signal, QEventLoop)
from time import sleep
from ip_utils.ipv4_edit import Ipv4Edit
from ip_utils.helpfunction import *
from ip_utils.ipv4Manager import Ipv4Manager
from .custom_widget import CustomSpinBoxTimer, CustomQSpinBoxCidr


class GameThreadIpv4Analyse(QThread):
    validateSignal = Signal(list)
    selectChallSignal = Signal()
    playSignal = Signal()

    def __init__(self, parent, timer:QLabel, randomIpv4:QLabel,
                 randomCidr:QLabel, buttonValidate:QPushButton, inputs:list):
        super().__init__(parent)
        self._buttonValidate = buttonValidate
        self._buttonValidate.clicked.connect(self.validate)
        self._isRunning = False
        self.timer = timer
        self._minutes = 0
        self._secondes = -1
        self._randomIpv4 = randomIpv4
        self._randomCidr = randomCidr
        self._inputs = inputs
        self.selectChallSignal.connect(self.selectChallMessage)
        self._timeOut = (60, 0)
        self.ipv4Edit:Ipv4Edit
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
        self._setIpv4Edit
        self._setIpv4Edit == self.ipv4Edit
        print(self.ipv4Edit.show_display)

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
        elif element == "Aléatoire":
            return None
        else:
            return element

    def generateChallenge(self, loop, options):
        self.accept = True
        if len(options) != 0:
            klass, reservation, ttype, cidr, time = options
            self.ipv4 = Ipv4Manager(self.translationDetect(klass), self.translationDetect(reservation), self.translationDetect(ttype), cidr).generateRandomIpv4()
            self._randomIpv4.setText(self.ipv4.ipHost)
            self._randomCidr.setText("/" + str(self.ipv4.cidr))
            self.setTimeOut(time)

        loop.quit()

    def selectChallMessage(self):
        options = SelectChallengeAnalyseIpv4(self.parent())
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
    def _setIpv4Edit(self):
        inputs = self._inputs
        ipv4EditList = [self.translationDetect(element.text() if isinstance(element, QLineEdit) else element.currentText()) for element in inputs]
        ipv4Edit = Ipv4Edit(
            *ipv4EditList
        )
        self.ipv4Edit = ipv4Edit
        self.ipv4Edit == self.ipv4


class SelectChallengeAnalyseIpv4(QDialog):
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
        self.comboBoxType.addItems([random, "@Réseau", "@Broadcast", "@Ipv4"])

        self.spinBoxCidr = CustomQSpinBoxCidr(self)

        layoutTime = QHBoxLayout(self)
        customSpinBoxTime = CustomSpinBoxTimer(self)
        self.spinBoxTimeMin, self.spinBoxTimeSec = customSpinBoxTime.min, customSpinBoxTime.sec
        layoutTime.addWidget(self.spinBoxTimeMin)
        layoutTime.addWidget(self.spinBoxTimeSec)

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

        self.comboBoxClass.currentIndexChanged.connect(self.classChanged)
        self.comboBoxReservation.currentIndexChanged.connect(self.reservationChanged)
        self.spinBoxCidr.valueChanged.connect(self.cidrChanged)

        self.setLayout(MainLayout)

        self.exec()

    def __bool__(self):
        return self.validated
    
    def classChanged(self):
        def simpleChoice():
            self.comboBoxReservation.addItems([random, "Privée", "Publique"])
        k = self.comboBoxClass.currentIndex()
        random = "Aléatoire"
        self.comboBoxReservation.clear()
        if k == 0:
            self.comboBoxReservation.addItems([random, "Privée", "Publique", "LocalHost", "Multicast", "IETF"])
        elif k == 1:
            simpleChoice()
        elif k == 2:
            simpleChoice()
            if self.spinBoxCidr.value() < 12 and self.spinBoxCidr.value() != 0:
                self.spinBoxCidr.setValue(12)
        elif k == 3:
            self.comboBoxReservation.addItems([random, "Privée", "Publique", "IETF"])
            if self.spinBoxCidr.value() < 16 and self.spinBoxCidr.value() != 0:
                self.spinBoxCidr.setValue(16)
        elif k == 4:
            self.comboBoxReservation.addItems(["Multicast"])
            if self.spinBoxCidr.value() < 4 and self.spinBoxCidr.value() != 0:
                self.spinBoxCidr.setValue(4)
        else:
            self.comboBoxReservation.addItems([random])
            if self.spinBoxCidr.value() < 4 and self.spinBoxCidr.value() != 0:
                self.spinBoxCidr.restricted((0, 4))

    def reservationChanged(self):
        # localhost minimal cidr is 8
        targetR = self.comboBoxReservation.currentText()
        targetC = self.comboBoxClass.currentText()
        value = self.spinBoxCidr.value()
        if (value != 24) and (targetR == "IETF"):
            self.spinBoxCidr.setValue(24)

        elif (targetC in ["D", "E"]) and isBadCidrForPrivate(targetC, value)  and (value != 0):
            self.spinBoxCidr.restricted((0, getMinimalCidrForPrivate(targetC)))
        elif (targetC == "A") and isBadCidrForPrivate(targetC, value) and (value != 0):
            self.spinBoxCidr.restricted((0, getMinimalCidrForPrivate(targetC)))
        elif (targetC == "B"):
            if (targetR == "Publique") and isBadCidrForPublic(targetC, value) and (value != 0):
                self.spinBoxCidr.restricted((0, getMinimalCidrForPublic(targetC)))
            else:
                if value != 0: self.spinBoxCidr.restricted((0, getMinimalCidrForPrivate(targetC)))
        elif (targetC == "C"):
            if (targetR == "Publique") and isBadCidrForPublic(targetC, value) and (value != 0):
                self.spinBoxCidr.restricted((0, getMinimalCidrForPublic(targetC)))
            else:
                if value != 0: self.spinBoxCidr.restricted((0, getMinimalCidrForPrivate(targetC)))
        elif (targetR == "LocalHost"):
            self.spinBoxCidr.restricted((0, 8))
        elif (targetC == "Aléatoire") and (targetR in ["Privée", "Publique"]):
            self.spinBoxCidr.setValue(0)
        else:
            self.spinBoxCidr.restricted((0, 4))
        """if targetR == "IETF" and value != 0:
            self.spinBoxCidr.setValue(24)
        elif targetC in ["D", "E"] and value < 4 and value != 0:
            self.spinBoxCidr.setValue(4)
        if targetC == "A" and targetR == "Privée" and value < 8 and value != 0:
            self.spinBoxCidr.setValue(8)  # ok
        elif targetR == "Privée" and targetC == "B" and value < 12 and value != 0:
            self.spinBoxCidr.setValue(12)  # ok
        elif targetR == "Privée" and targetC == "C" and value < 16 and value != 0:
            self.spinBoxCidr.setValue(16)  # ok
        elif targetR == "LocalHost" and value < 8 and value != 0:
            self.spinBoxCidr.setValue(8)

        elif targetC == "C" and value < 2 and value != 0:
            self.spinBoxCidr.setValue(2)
        elif targetC == "Aléatoire" and targetR in ["Privée", "Publique"]:
            self.spinBoxCidr.setValue(0)
        self.spinBoxCidr.restricted((0, 4))"""

    def cidrChanged(self):
        value = self.spinBoxCidr.value()
        targetR = self.comboBoxReservation.currentText()
        targetC = self.comboBoxClass.currentText()
        if (value != 24) and (targetR == "IETF"):
            self.spinBoxCidr.setValue(24)

        elif (targetC in ["D", "E"]) and isBadCidrForPrivate(targetC, value)  and (value != 0):
            self.spinBoxCidr.restricted((0, getMinimalCidrForPrivate(targetC)))
        elif (targetC == "A") and isBadCidrForPrivate(targetC, value) and (value != 0):
            self.spinBoxCidr.restricted((0, getMinimalCidrForPrivate(targetC)))
        elif (targetC == "B"):
            if (targetR == "Publique") and isBadCidrForPublic(targetC, value) and (value != 0):
                self.spinBoxCidr.restricted((0, getMinimalCidrForPublic(targetC)))
            else:
                if value != 0: self.spinBoxCidr.restricted((0, getMinimalCidrForPrivate(targetC)))
        elif (targetC == "C"):
            if (targetR == "Publique") and isBadCidrForPublic(targetC, value) and (value != 0):
                self.spinBoxCidr.restricted((0, getMinimalCidrForPublic(targetC)))
            else:
                if value != 0: self.spinBoxCidr.restricted((0, getMinimalCidrForPrivate(targetC)))
        elif (targetR == "LocalHost"):
            self.spinBoxCidr.restricted((0, 8))
        elif (targetC == "Aléatoire") and (targetR in ["Privée", "Publique"]):
            self.spinBoxCidr.setValue(0)
        else:
            self.spinBoxCidr.restricted((0, 4))

    def setValidated(self):
        self.validated = True

    def validate_choices(self):
        choiceClass = self.comboBoxClass.currentText()
        choiceReservation = self.comboBoxReservation.currentText()
        choiceType = self.comboBoxType.currentText()
        choiceCidr = self.spinBoxCidr.value()
        choiceTime = self.spinBoxTimeMin.value(), self.spinBoxTimeSec.value()
        self.accept()
        self.choices = [choiceClass, choiceReservation, choiceType, choiceCidr, choiceTime]
        self.setValidated()

