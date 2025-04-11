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


class CustomSpinBoxTimer:
    def __init__(self, parent):
        self._min = CustomQSpinBox(parent=parent)
        self._min.setSuffix(" min")
        self._min.setMaximum(60)
        self._min.valueChanged.connect(self.changeMinute)
        self._sec = CustomQSpinBox(parent=parent)
        self._sec.setMaximum(60)
        self._sec.setSuffix(" s")
        self._sec.valueChanged.connect(self.changeSecond)
        self.min.setValue(2)

    @property
    def min(self):
        return self._min
    
    @property
    def sec(self):
        return self._sec
    
    def changeSecond(self):
        if self.sec.value() < 30 and self.min.value() == 0:
            self.sec.setValue(30)
        elif self.min.value() == 60:
            self.sec.setValue(0)

    def changeMinute(self):
        if self.min.value() == 60:
            self.sec.setValue(0)
        self.changeSecond()
