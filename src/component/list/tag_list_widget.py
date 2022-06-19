from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QFont, QFontMetrics
from PySide2.QtWidgets import QListWidgetItem, QLabel, QAbstractItemView

from component.list.base_list_widget import BaseListWidget
from component.scroll.smooth_scroll_bar import SmoothScrollBar


class TagListWidget(BaseListWidget):
    def __init__(self, parent):
        BaseListWidget.__init__(self, parent)
        self.setViewMode(self.ViewMode.ListMode)
        self.setFlow(self.Flow.LeftToRight)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setMaximumHeight(30)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.hScrollBar = SmoothScrollBar()
        self.hScrollBar.setOrientation(Qt.Orientation.Horizontal)
        self.setHorizontalScrollBar(self.hScrollBar)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.horizontalScrollBar().setSingleStep(30)

    def wheelEvent(self, arg__1) -> None:
        self.hScrollBar.ScrollValue(-arg__1.angleDelta().y())

    def AddItem(self, name, isSelectable=False):
        label = QLabel(name)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color:#d5577c")
        # font = QFont()
        # font.setPointSize(12)
        # font.setBold(True)
        # label.setFont(font)

        item = QListWidgetItem(self)
        item.setTextAlignment(Qt.AlignCenter)
        # item.setBackground(QColor(87, 195, 194))
        # item.setBackground(QColor(0, 0, 0, 0))
        fm = QFontMetrics(item.font())

        width = fm.boundingRect(name).width()
        height = fm.height()
        self.setItemWidget(item, label)
        item.setSizeHint(QSize(width, height) + QSize(20, 0))
        if not isSelectable:
            item.setFlags(item.flags() & (~Qt.ItemIsSelectable))
