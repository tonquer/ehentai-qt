from PySide6.QtCore import QByteArray, QBuffer, QTimer, Qt
from PySide6.QtGui import QMovie, QPixmap, QImage
from PySide6.QtWidgets import QLabel


class GifGroupLabel(QLabel):
    def __init__(self, parent):
        QLabel.__init__(self, parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.images = []
        self.index = 0

    def Init(self):
        for i in range(10):
            image = QImage(":/png/icon/loading/loading_{}.png".format(i+1))
            self.images.append(image)

    def ShowNextPixMap(self):
        if not self.images:
            return
        if self.index >= len(self.images):
            self.index = 0
        image = self.images[self.index]
        p = QPixmap(image)
        radio = self.devicePixelRatioF()
        p.setDevicePixelRatio(radio)
        self.setPixmap(p)
        self.index += 1
