from PySide6.QtCore import QByteArray, QBuffer, Qt, QTimer
from PySide6.QtGui import QMovie, QPixmap
from PySide6.QtWidgets import QLabel


class GifLabel(QLabel):
    def __init__(self, parent):
        QLabel.__init__(self, parent)
        self.movie = QMovie()
        self.byteArray = None
        self.bBuffer = None
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        # self.movie.frameChanged.connect(self.FrameChange)
        self.timer = QTimer()
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.DelayTimeout)

    def FrameChange(self):
        currentPixmap = self.movie.currentPixmap()
        size = currentPixmap.size()
        radioF = self.devicePixelRatioF()
        pixmap = QPixmap()
        pixmap.setDevicePixelRatio(radioF)
        self.setPixmap(pixmap)
        return

    def delayHide(self, delay=250):
        if self.timer.isActive():
            return
        if self.isHidden():
            return
        self.timer.setInterval(delay)
        self.timer.start()
        return

    def DelayTimeout(self):
        self.timer.stop()
        self.hide()

    def Init(self, data):
        self.resize(250, 250)
        self.byteArray = QByteArray(data)
        self.bBuffer = QBuffer(self.byteArray)

        # self.movie.setFormat(QByteArray(b"WEBP"))

        self.movie.setCacheMode(QMovie.CacheMode.CacheNone)
        self.movie.setDevice(self.bBuffer)
        # self.movie.setSpeed(100)
        self.setMovie(self.movie)

        self.movie.start()
        self.setScaledContents(True)

    def InitByFileName(self, name):
        self.resize(300, 300)
        self.movie = QMovie(name)
        # self.movie.setFileName(name)
        self.movie.setFormat(QByteArray(b"GIF"))
        self.movie.start()
        return
