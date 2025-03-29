from PySide6.QtWidgets import (QSpinBox)


class CustomQSpinBox(QSpinBox):
    def __init__(self, parent):
        super().__init__(parent)

    def textFromValue(self, value):
        return f"{value:02}"


class CustomQSpinBoxCidr(QSpinBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMinimum(0)
        self.setMaximum(30)
        self._increment = 0
    
    def restricted(self, rangeValue:tuple):
        increment = self._increment
        minValue = min(rangeValue)
        maxvalue = max(rangeValue)
        if increment:
            if (increment < 0) and (self.value() < maxvalue):
                self.setValue(minValue)
            elif (0 < increment) and (self.value() < maxvalue):
                self.setValue(maxvalue)

    def stepBy(self, steps):
        self.setIncrement(0)
        if steps < 0:
            self.setIncrement(-1)
        elif 0 < steps:
            self.setIncrement(1)
        self.setValue(self.value() + steps)
        self.selectAll()
    
    def setIncrement(self, increment):
        self._increment = increment

    def wheelEvent(self, event):
        changeValue = event.angleDelta().y() // 120
        self.setIncrement(0)
        if 0 < changeValue and self.value() < self.maximum():
            self.setIncrement(1)
        elif changeValue < 0 and self.minimum() - 1 < self.value():
            self.setIncrement(-1)
        self.setValue(self._increment + self.value())
        self.selectAll()
