from PySide6.QtWidgets import (QLabel, QLineEdit, QPushButton)
from PySide6.QtCore import (QThread, Signal)
from time import sleep


class GameThreadIpAnalyse(QThread):
    finished = Signal()

    def __init__(self, parent, timer:QLabel, randomIp:QLabel,
                 randomCidr:QLabel, buttonValidate:QPushButton, inputs:list):
        super().__init__(parent)
        self._buttonValidate = buttonValidate
        self._buttonValidate.clicked.connect(self.stop)
        self._isRunning = False
        self.timer = timer
        self._minutes = 0
        self._secondes = -1

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

    def reset(self):
        self._minutes = 0
        self._secondes = -1
        self._isRunning = True

    def run(self):
        self.reset()
        self._buttonValidate.setEnabled(True)
        while self.isRunning:
            self._addSeconde
            self.timer.setText(f"{self.minutes:02}:{self.secondes:02}")
            sleep(1)

    def generateChallenge(self):
        pass
