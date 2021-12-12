from PySide2.QtWidgets import QSlider


class WheelSlider(QSlider):
    def __init__(self, parent=None):
        QSlider.__init__(self, parent)

    def wheelEvent(self, event):
        event.ignore()
