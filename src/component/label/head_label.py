from PySide6.QtCore import Qt
from PySide6.QtGui import QPainterPath, QPixmap, QPainter
from PySide6.QtWidgets import QLabel


class HeadLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super(HeadLabel, self).__init__(*args, **kwargs)
        self.antialiasing = True
        self.radius = 100
        self.target = None

    def SetPicture(self, data, titleData=None):
        self.target = QPixmap(self.size())  # 大小和控件一样
        self.target.fill(Qt.GlobalColor.transparent)  # 填充背景为透明
        q = QPixmap()
        q.loadFromData(data)
        radio = self.devicePixelRatioF()
        q.setDevicePixelRatio(radio)

        offset = 0
        if titleData:
            offset = 20

        p = q.scaled(  # 加载图片并缩放和控件一样大
            (self.width()-offset)*radio, (self.height()-offset)*radio, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)

        painter = QPainter(self.target)
        if self.antialiasing:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            # painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

        path = QPainterPath()
        path.addRoundedRect(
            offset//2, offset//2, self.width()-offset, self.height()-offset, self.radius, self.radius)
        painter.setClipPath(path)

        painter.drawPixmap(offset//2, offset//2, p)
        self.setPixmap(self.target)

        if titleData:
            p = QPixmap()
            p.loadFromData(titleData)
            p.setDevicePixelRatio(self.devicePixelRatioF())
            titleP = p.scaled(  # 加载图片并缩放和控件一样大
                self.height(), self.width(), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
            painter = QPainter()
            painter.begin(titleP)
            painter.setCompositionMode(QPainter.CompositionMode_DestinationOver)
            painter.drawPixmap(0, 0, self.target)
            painter.end()

            self.target = QPixmap(self.size())  # 大小和控件一样
            self.target.fill(Qt.GlobalColor.transparent)  # 填充背景为透明
            painter.begin(self.target)
            painter.drawPixmap(0, 0, titleP)
            painter.end()
            self.setPixmap(self.target)