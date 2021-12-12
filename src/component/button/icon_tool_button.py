from PySide2.QtWidgets import QToolButton


class IconToolButton(QToolButton):
    def __init__(self, parent=None):
        QToolButton.__init__(self, parent)