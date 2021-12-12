from PySide2.QtCore import Qt
from PySide2.QtGui import QWheelEvent
from PySide2.QtWidgets import QScrollArea

from component.scroll.smooth_scroll_bar import SmoothScrollBar


class SmoothScrollArea(QScrollArea):
    """ 一个可以平滑滚动的区域 """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.count = 0
        self.vScrollBar = SmoothScrollBar()
        self.vScrollBar.setOrientation(Qt.Orientation.Vertical)
        self.setVerticalScrollBar(self.vScrollBar)

    def wheelEvent(self, arg__1: QWheelEvent) -> None:
        self.vScrollBar.ScrollValue(-arg__1.angleDelta().y())
