from PySide6 import QtCore
from PySide6.QtCore import QByteArray, QBuffer, Qt, QTimer
from PySide6.QtGui import QMovie, QPixmap
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QLabel


class LoadingLabel(QSvgWidget):
    def __init__(self, parent):
        QSvgWidget.__init__(self, parent)
        self.load(":/png/icon/loading.svg")
        self.resize(self.renderer().defaultSize())
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        isGif = self.renderer().animated()
        isGif