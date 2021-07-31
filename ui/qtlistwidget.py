from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QPixmap, QColor, QFont, QCursor
from PySide2.QtWidgets import QListWidget, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QListWidgetItem, QAbstractSlider, \
    QScroller, QMenu, QApplication, QAbstractItemView

from conf import config
from resources.resources import DataMgr
from src.qt.com.qtcomment import QtComment
from src.qt.com.qtimg import QtImgMgr
from src.qt.qt_main import QtOwner
from src.qt.util.qttask import QtTaskBase
from src.util.status import Status


class ItemWidget(QWidget):
    def __init__(self, _id, title, leftStr1="", leftStr2="", leftStr3="", leftStr4=""):
        super(ItemWidget, self).__init__()
        self.id = _id
        self.url = ""
        self.path = ""
        self.IsClicked = False
        # self.setMaximumSize(220, 400)
        # self.setMaximumSize(220, 550)
        layout = QVBoxLayout(self)
        # layout.setContentsMargins(10, 10, 10, 0)
        # 图片label
        self.pictureData = None
        self.picIcon = QLabel(self)
        # self.picIcon.setCursor(Qt.PointingHandCursor)
        # self.picIcon.setScaledContents(True)
        self.picIcon.setMinimumSize(220, 308)
        self.picIcon.setMaximumSize(220, 308)

        self.picIcon.setToolTip(title)
        pic = QPixmap()
        self.picIcon.setPixmap(pic)
        layout.addWidget(self.picIcon)
        if leftStr1:
            self.leftLabel1 = QLabel(leftStr1, self)
            self.leftLabel1.setMinimumHeight(20)
            self.leftLabel1.setMaximumHeight(50)
            self.leftLabel1.setWordWrap(True)
            self.leftLabel1.adjustSize()
            self.leftLabel1.setAlignment(Qt.AlignLeft)
            layout.addWidget(self.leftLabel1)

        if leftStr2:
            layout2 = QHBoxLayout()
            p = QPixmap()
            p.loadFromData(DataMgr.GetData("icon_bookmark_on"))
            self.starPic = QLabel()

            self.starPic.setMinimumSize(20, 20)
            self.starPic.setMaximumSize(20, 20)
            self.starPic.setPixmap(p)
            self.starPic.setCursor(Qt.PointingHandCursor)
            self.starPic.setScaledContents(True)

            self.leftLabel2 = QLabel(leftStr2, self)
            self.leftLabel2.setMinimumHeight(20)
            self.leftLabel2.setMaximumHeight(20)
            self.leftLabel2.setAlignment(Qt.AlignLeft)
            self.leftLabel2.adjustSize()

            layout2.addWidget(self.starPic)
            layout2.addWidget(self.leftLabel2)
            if leftStr3:
                self.leftLabel3 = QLabel(leftStr3, self)
                self.leftLabel3.setMinimumHeight(20)
                self.leftLabel3.setMaximumHeight(20)
                self.leftLabel3.setAlignment(Qt.AlignRight)
                self.leftLabel3.adjustSize()
                layout2.addWidget(self.leftLabel3)

            layout.addLayout(layout2)

        if leftStr4:
            self.leftLabel4 = QLabel(leftStr4, self)
            self.leftLabel4.setMinimumHeight(20)
            self.leftLabel4.setMaximumHeight(20)
            self.leftLabel4.adjustSize()
            self.leftLabel4.setAlignment(Qt.AlignLeft)
            layout.addWidget(self.leftLabel4)

        self.label = QLabel(title, self)
        self.label.setMinimumSize(210, 20)
        self.label.setMaximumSize(210, 150)
        self.label.setAlignment(Qt.AlignLeft)
        self.label.adjustSize()
        self.label.setWordWrap(True)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

    def SetPicture(self, data):
        if not data:
            return
        self.pictureData = data
        pic = QPixmap()
        pic.loadFromData(data)
        newPic = pic.scaled(self.picIcon.width(), self.picIcon.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.picIcon.setPixmap(newPic)

    def GetTitle(self):
        return self.label.text()

    def GetId(self):
        return self.id


class QtBookList(QListWidget, QtTaskBase):
    def __init__(self, parent):
        QListWidget.__init__(self, parent)
        QtTaskBase.__init__(self)
        self.page = 1
        self.pages = 1
        self.verticalScrollBar().actionTriggered.connect(self.OnActionTriggered)
        # self.verticalScrollBar().valueChanged.connect(self.OnMove)
        self.isLoadingPage = False
        self.LoadCallBack = None
        self.parentId = -1
        self.popMenu = None
        QScroller.grabGesture(self, QScroller.LeftMouseButtonGesture)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # self.verticalScrollBar().setStyleSheet(QssDataMgr().GetData('qt_list_scrollbar'))
        self.verticalScrollBar().setSingleStep(30)

    def InitBook(self, callBack=None):
        self.resize(800, 600)
        self.setMinimumHeight(400)
        self.setFrameShape(self.NoFrame)  # 无边框
        self.setFlow(self.LeftToRight)  # 从左到右
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)
        self.LoadCallBack = callBack

        self.popMenu = QMenu(self)
        action = self.popMenu.addAction("打开")
        action.triggered.connect(self.OpenBookInfoHandler)
        action = self.popMenu.addAction("查看封面")
        action.triggered.connect(self.OpenPicture)
        action = self.popMenu.addAction("重下封面")
        action.triggered.connect(self.ReDownloadPicture)
        action = self.popMenu.addAction("复制标题")
        action.triggered.connect(self.CopyHandler)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.doubleClicked.connect(self.OpenBookInfo)
        self.customContextMenuRequested.connect(self.SelectMenu)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def InstallCategory(self):
        self.doubleClicked.disconnect(self.OpenBookInfo)
        self.popMenu = QMenu(self)
        action = self.popMenu.addAction("查看封面")
        action.triggered.connect(self.OpenPicture)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        return

    def InstallDel(self):
        action = self.popMenu.addAction("刪除")
        action.triggered.connect(self.DelHandler)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def InitUser(self, callBack=None):
        self.setFrameShape(self.NoFrame)  # 无边框
        self.LoadCallBack = callBack
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def OnActionTriggered(self, action):
        if action != QAbstractSlider.SliderMove or self.isLoadingPage:
            return
        if self.page >= self.pages:
            return
        if self.verticalScrollBar().sliderPosition() == self.verticalScrollBar().maximum():
            self.isLoadingPage = True
            if self.LoadCallBack:
                self.LoadCallBack()

    def UpdatePage(self, page, pages):
        self.page = page
        self.pages = pages

    def UpdateState(self, isLoading=False):
        self.isLoadingPage = isLoading

    def AddBookItem(self, _id, title, info="", url="", path="", param="", originalName=""):
        index = self.count()
        iwidget = ItemWidget(_id, title)
        iwidget.url = url
        iwidget.path = path
        item = QListWidgetItem(self)
        item.setSizeHint(iwidget.sizeHint())
        self.setItemWidget(item, iwidget)
        iwidget.picIcon.setText("图片加载中...")
        if url and config.IsLoadingPicture:
            self.AddDownloadTask(url, path, None, self.LoadingPictureComplete, True, index, True)
            pass

    def AddUserItem(self, commnetId, commentsCount, likesCount, content, name, createdTime, floor, url="", path="", originalName="", title="", level=1):
        index = self.count()
        iwidget = QtComment(self)
        iwidget.id = commnetId
        iwidget.commentLabel.setText(content)
        iwidget.nameLabel.setText(name)
        # iwidget.numLabel.setText("({})".format(commentsCount))
        # iwidget.starLabel.setText("({})".format(likesCount))
        iwidget.levelLabel.setText(" LV" + str(level) + " ")
        iwidget.titleLabel.setText(" " + title + " ")
        iwidget.dateLabel.setText("{}".format(createdTime))

        iwidget.indexLabel.setText("{}楼".format(str(floor)))

        item = QListWidgetItem(self)
        item.setSizeHint(iwidget.sizeHint())
        self.setItemWidget(item, iwidget)
        if url and config.IsLoadingPicture:
            self.AddDownloadTask(url, path, None, self.LoadingPictureComplete, True, index, True)
            pass

    def LoadingPictureComplete(self, data, status, index):
        if status == Status.Ok:
            item = self.item(index)
            widget = self.itemWidget(item)
            widget.SetPicture(data)
            pass
        else:
            item = self.item(index)
            widget = self.itemWidget(item)
            widget.picIcon.setText("图片加载失败")
        return

    def clear(self) -> None:
        QListWidget.clear(self)

        # 防止异步加载时，信息错乱
        self.ClearTask()

    def SelectMenu(self, pos):
        index = self.indexAt(pos)
        if index.isValid():
            self.popMenu.exec_(QCursor.pos())
        pass

    def DownloadHandler(self):
        selected = self.selectedItems()
        for item in selected:
            widget = self.itemWidget(item)
            QtOwner().owner.epsInfoForm.OpenEpsInfo(widget.GetId())
        pass

    def OpenBookInfoHandler(self):
        selected = self.selectedItems()
        for item in selected:
            widget = self.itemWidget(item)
            QtOwner().owner.bookInfoForm.OpenBook(widget.GetId())
            return

    def CopyHandler(self):
        selected = self.selectedItems()
        if not selected:
            return

        data = ''
        for item in selected:
            widget = self.itemWidget(item)
            data += widget.GetTitle() + str("\r\n")
        clipboard = QApplication.clipboard()
        data = data.strip("\r\n")
        clipboard.setText(data)
        pass

    def DelHandler(self):
        bookIds = set()
        selected = self.selectedItems()
        for item in selected:
            widget = self.itemWidget(item)
            bookIds.add(widget.GetId())
        if not bookIds:
            return
        self.parent().DelCallBack(bookIds)

    def OpenBookInfo(self, modelIndex):
        index = modelIndex.row()
        item = self.item(index)
        if not item:
            return
        widget = self.itemWidget(item)
        if not widget:
            return
        bookId = widget.id
        if not bookId:
            return
        QtOwner().owner.bookInfoForm.OpenBook(bookId)

    def OpenPicture(self):
        selected = self.selectedItems()
        for item in selected:
            widget = self.itemWidget(item)
            QtImgMgr().ShowImg(widget.pictureData)
            return

    def ReDownloadPicture(self):
        selected = self.selectedItems()
        for item in selected:
            widget = self.itemWidget(item)
            index = self.row(item)
            if widget.url and config.IsLoadingPicture:
                widget.picIcon.setPixmap(None)
                widget.picIcon.setText("图片加载中")
                self.AddDownloadTask(widget.url, "", None, self.LoadingPictureComplete, True, index, False)
                pass


class QtCategoryList(QListWidget):
    def __init__(self, parent):
        QListWidget.__init__(self, parent)
        self.setViewMode(self.ListMode)
        self.setFlow(self.LeftToRight)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollMode(self.ScrollPerItem)
        QScroller.grabGesture(self, QScroller.LeftMouseButtonGesture)
        self.setMaximumHeight(30)
        self.setFocusPolicy(Qt.NoFocus)

    def AddItem(self, name):
        item = QListWidgetItem(name)
        item.setTextAlignment(Qt.AlignCenter)
        # item.setBackground(QColor(87, 195, 194))
        item.setBackground(QColor(0, 0, 0, 0))
        item.setSizeHint(QSize(90, 30))
        item.setFlags(item.flags() & (~Qt.ItemIsSelectable))

        self.addItem(item)

    def ClickItem(self, item):
        if item.background().color() == QColor(0, 0, 0, 0):
            item.setBackground(QColor(87, 195, 194))
            return True
        else:
            item.setBackground(QColor(0, 0, 0, 0))
            return False

    def GetAllSelectItem(self):
        data = set()
        for i in range(self.count()):
            item = self.item(i)
            if item.background().color() == QColor(87, 195, 194):
                data.add(item.text())
        return data
