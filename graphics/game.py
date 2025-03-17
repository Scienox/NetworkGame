from PySide6.QtWidgets import (QLabel, QLineEdit, QPushButton)
from PySide6.QtCore import (QThread, Signal)
from time import sleep
from ip_untils.ip_edit import IpEdit
from ip_untils.ip import IP


class GameThreadIpAnalyse(QThread):
    finished = Signal()

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
        self.finished.emit()
        self._isRunning = False
        self._buttonValidate.setEnabled(False)

    def reset(self):
        self._minutes = 0
        self._secondes = -1
        [self.translationDetect(element.setText('') if isinstance(element, QLineEdit) else element.setCurrentIndex(0)) for element in self._inputs]
        [element.setEnabled(True) for element in self._inputs]
        self._isRunning = True

    def run(self):
        self.reset()
        self._buttonValidate.setEnabled(True)
        self.generateChallenge()
        while self.isRunning:
            self._addSeconde
            self.timer.setText(f"{self.minutes:02}:{self.secondes:02}")
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

    def generateChallenge(self, type=None, class_=None, time=None):
        self.ip = IP("192.168.0.5", 24)

        self._randomIp.setText(self.ip.ipHost)
        self._randomCidr.setText('/' + str(self.ip.cidr))

    def validate(self):
        inputs = self._inputs
        ipEditList = [self.translationDetect(element.text() if isinstance(element, QLineEdit) else element.currentText()) for element in inputs]
        ipEdit = IpEdit(
            *ipEditList
        )
        [element.setEnabled(False) for element in self._inputs]
        ipEdit == self.ip
        print(ipEdit.show_display)
        self.stop()
 