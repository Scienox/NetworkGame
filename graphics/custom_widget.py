from PySide6.QtWidgets import (QSpinBox)


class CustomQSpinBox(QSpinBox):
    def __init__(self, parent):
        super().__init__(parent)

    def textFromValue(self, value):
        return f"{value:02}"
    