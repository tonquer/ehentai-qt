import json

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt, QSize, QEvent
from PySide2.QtGui import QFont, QPixmap, QIcon
from PySide2.QtWidgets import QListWidgetItem, QLabel, QDesktopWidget

from config.setting import Setting
from interface.ui_book_info import Ui_BookInfo
from qt_owner import QtOwner
from server import req, Log, config
from util.status import Status
from task.qt_task import QtTaskBase
from tools.book import BookMgr
from tools.str import Str


class BookInfoView(QtWidgets.QWidget, Ui_BookInfo, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_BookInfo.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.bookId = ""
        self.token = ""
        self.site = ""
        self.url = ""
        self.path = ""
        self.bookName = ""
        self.lastEpsId = -1
        self.pictureData = None

        self.picture.installEventFilter(self)
        self.title.setWordWrap(True)
        self.title.setTextInteractionFlags(Qt.TextSelectableByMouse)
        # self.epsListWidget.setFlow(self.epsListWidget.LeftToRight)
        self.epsListWidget.setWrapping(True)
        self.epsListWidget.wheelMode = 1
        self.epsListWidget.setViewMode(self.epsListWidget.ViewMode.ListMode)
        self.epsListWidget.setFlow(self.epsListWidget.Flow.TopToBottom)
        self.epsListWidget.setFrameShape(self.epsListWidget.NoFrame)
        self.epsListWidget.setResizeMode(self.epsListWidget.Adjust)

        self.commentButton.clicked.connect(self.OpenComment)

        data = str(QtOwner().GetFileData(":/json/translate.json"), encoding="utf-8")
        self.tags = json.loads(data)

        self.epsListWidget.itemClicked.connect(self.ClickTagsItem)
        self.nameToTag = {}

    def Clear(self):
        self.ClearTask()
        self.epsListWidget.clear()
        self.nameToTag.clear()

    def SwitchCurrent(self, **kwargs):
        bookId = kwargs.get("bookId")
        token = kwargs.get("token", "")
        site = kwargs.get("site", "")
        if not bookId:
            return

        self.OpenBook(bookId, token, site)

    def OpenBook(self, bookId, token="", site=""):
        self.bookId = bookId
        self.site = site
        if not self.site:
            self.site = config.CurSite
        self.Clear()
        QtOwner().ShowLoading()
        QtOwner().SetDirty()
        self.AddHttpTask(req.BookInfoReq(bookId, token=token, site=self.site), self.OpenBookBack)

    def OpenBookBack(self, data):
        QtOwner().CloseLoading()
        st = data.get("st")
        if st == Status.Ok:
            maxPages = data.get("maxPages")
            # self.listWidget.UpdatePage(1, maxPages)
            # self.listWidget.UpdateState()
            self.epsListWidget.clear()
            info = BookMgr().GetBookBySite(self.bookId, self.site)
            self.title.setText(info.baseInfo.title)
            self.bookName = info.baseInfo.title
            self.token = info.baseInfo.token
            self.picture.setText(Str.GetStr(Str.LoadingPicture))
            self.url = info.baseInfo.imgUrl
            self.path = ""
            self.idLabel.setText(self.bookId)
            self.updateTick.setText(info.pageInfo.posted)
            self.favoriteLabel.setText(str(info.pageInfo.favorites))
            self.pageLabel.setText(str(info.pageInfo.pages))
            self.lanLabel.setText(info.pageInfo.language)
            self.categoryList.AddItem(info.baseInfo.category)
            self.commentButton.setText("({})".format(len(info.pageInfo.comment)))
            for tag in info.baseInfo.tags:
                tagData = tag.split(":")
                if len(tagData) >= 2:
                    tagName = tagData[0]
                    if not tagName:
                        tag = "misc" + tag

                label = QLabel(tag)
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet("color: rgb(196, 95, 125);")
                font = QFont()
                font.setPointSize(12)
                font.setBold(True)
                label.setFont(font)

                item = QListWidgetItem(self.epsListWidget)
                item.setSizeHint(label.sizeHint() + QSize(20, 20))

                tagData = tag.split(":")
                if Setting.Language.autoValue != 3:
                    if len(tagData) >= 2:
                        tagName = tagData[0]
                        if tagName in self.tags:
                            if tagData[1] in self.tags.get(tagName, {}).get("data"):
                                tagInfo = self.tags.get(tagName, {}).get("data", {}).get(tagData[1], {})
                                label.setText(self.tags.get(tagName, {}).get("name", "") + ":" + tagInfo.get("dest", ""))
                                item.setToolTip(tagInfo.get('description', ""))

                # item.setToolTip(epsInfo.title)
                self.epsListWidget.setItemWidget(item, label)
                self.nameToTag[label.text()] = tag

            if config.IsLoadingPicture:
                self.AddDownloadTask(self.url, "{}/{}_{}_cover".format(config.CurSite, self.bookId, self.token), completeCallBack=self.UpdatePicture)

        else:
            msg = data.get("msg")
            if msg:
                QtOwner().ShowError(msg)
            else:
                QtOwner().ShowError(Str.GetStr(st))
        return

    def UpdatePicture(self, data, status):
        if status == Status.Ok:
            self.pictureData = data
            pic = QtGui.QPixmap()
            pic.loadFromData(data)
            pic.scaled(self.picture.size(), QtCore.Qt.KeepAspectRatio)
            self.picture.setPixmap(pic)
            # self.picture.setScaledContents(True)
            self.update()
        else:
            self.picture.setText(Str.GetStr(Str.LoadingFail))
        return

    def LoadNextPage(self):
        return

    def StartRead(self):
        QtOwner().OpenReadView(self.bookId, self.title.text(), -1)
        return

    def LoadHistory(self):
        return

    def ClickTagsItem(self, item):
        widget = self.epsListWidget.itemWidget(item)
        text = self.nameToTag.get(widget.text())
        data = text.split("|")
        if data[0]:
            text = data[0]
        text = text.strip("|").strip("$")
        text2 = text.split(":")
        if len(text2) >= 2:
            newText = text2[0] + ":\"" + text2[1] + "$\""
        else:
            newText = text+"$"

        QtOwner().OpenSearch(newText)
        return

    def OpenComment(self):
        QtOwner().OpenComment(self.bookId, self.site)
        return

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                if self.pictureData:
                    QtOwner().OpenWaifu2xTool(self.pictureData)
                return True
            else:
                return False
        else:
            return super(self.__class__, self).eventFilter(obj, event)

    def AddFavorite(self):
        if not config.CurLoginName:
            QtOwner().ShowError(Str.GetStr(Str.NotLogin))
            return
        QtOwner().OpenFavoriteInfo(self.bookId, self.bookName)
        return

    def AddDownload(self):
        bookId = self.bookId
        info = BookMgr().GetBookBySite(bookId, self.site)
        QtOwner().downloadView.AddDownload(bookId, info.baseInfo.token, config.CurSite)
        QtOwner().ShowMsg(Str.GetStr(Str.AddDownload))