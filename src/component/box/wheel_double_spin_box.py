from PySide2.QtWidgets import QDoubleSpinBox


class WheelDoubleSpinBox(QDoubleSpinBox):
    def __init__(self, parent=None):
        QDoubleSpinBox.__init__(self, parent)

    def wheelEvent(self, event):
        event.ignore()

