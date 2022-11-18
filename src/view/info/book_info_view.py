import json
from functools import partial

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt, QSize, QEvent, Signal
from PySide2.QtGui import QColor, QFont, QPixmap, QIcon
from PySide2.QtWidgets import QListWidgetItem, QLabel, QDesktopWidget, QPushButton, QVBoxLayout, QSpacerItem, \
    QSizePolicy

import config.config
from component.layout.flow_layout import FlowLayout
from config.setting import Setting
from interface.ui_book_info import Ui_BookInfo
from qt_owner import QtOwner
from server import req, Log, config
from util.status import Status
from task.qt_task import QtTaskBase
from tools.book import BookMgr
from tools.str import Str


class BookInfoView(QtWidgets.QWidget, Ui_BookInfo, QtTaskBase):
    ReloadHistory = Signal()

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
        self.lastIndex = 0
        self.pictureData = None

        self.picture.installEventFilter(self)
        self.title.setWordWrap(True)
        self.title.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.allFlowLayout = []
        self.allFlowLabel = []
        self.flowHorizontalSpacer = None
        # self.epsListWidget.setFlow(self.epsListWidget.LeftToRight)
        # self.epsListWidget.setWrapping(True)
        # self.epsListWidget.wheelMode = 1
        # self.epsListWidget.setViewMode(self.epsListWidget.ViewMode.ListMode)
        # self.epsListWidget.setFlow(self.epsListWidget.Flow.TopToBottom)
        # self.epsListWidget.setFrameShape(self.epsListWidget.NoFrame)
        # self.epsListWidget.setResizeMode(self.epsListWidget.Adjust)

        self.commentButton.clicked.connect(self.OpenComment)

        data = str(QtOwner().GetFileData(":/json/translate.json"), encoding="utf-8")
        self.tags = json.loads(data)

        # self.epsListWidget.itemClicked.connect(self.ClickTagsItem)
        self.nameToTag = {}
        self.ReloadHistory.connect(self.LoadHistory)
        self.tabWidget.setCurrentIndex(0)
        self.preListWidget.LoadCallBack = self.LoadNextPage

    def Clear(self):
        self.ClearTask()
        self.preListWidget.clear()
        # self.epsListWidget.clear()
        self.nameToTag.clear()
        self.tabWidget.setCurrentIndex(0)

    def SwitchCurrent(self, **kwargs):
        bookId = kwargs.get("bookId")
        token = kwargs.get("token", "")
        site = kwargs.get("site", "")
        task = kwargs.get("task")
        if task:
            self.OpenBookByDownloadTask(task)
            return

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
        self.startRead.setEnabled(False)
        self.AddHttpTask(req.BookInfoReq(bookId, token=token, site=self.site), self.OpenBookBack)

    def OpenBookByDownloadTask(self, task):
        from view.download.download_item import DownloadItem
        assert isinstance(task, DownloadItem)
        self.Clear()
        self.bookId = task.bookId
        self.bookName = task.title
        self.token = task.token
        self.site = task.site
        self.idLabel.setText("https://{}.org/g/{}/{}".format(self.site, self.bookId, self.token))
        self.title.setText(self.bookName)

        if QtOwner().isOfflineModel:
            self.startRead.setEnabled(True)
            self.AddDownloadTask(self.url, self.GetCoverKey(self.bookId, self.token, config.CurSite), completeCallBack=self.UpdatePicture)
            return
        self.startRead.setEnabled(False)
        self.AddHttpTask(req.BookInfoReq(self.bookId, token=self.token, site=self.site), self.OpenBookBack)
        return

    def OpenBookBack(self, data):
        QtOwner().CloseLoading()
        st = data.get("st")
        if st == Status.Ok:
            self.startRead.setEnabled(True)
            maxPages = data.get("maxPages")
            # self.listWidget.UpdatePage(1, maxPages)
            # self.listWidget.UpdateState()
            # self.epsListWidget.clear()
            info = BookMgr().GetBookBySite(self.bookId, self.site)
            self.title.setText(info.baseInfo.title)
            self.bookName = info.baseInfo.title
            self.token = info.baseInfo.token
            self.picture.setText(Str.GetStr(Str.LoadingPicture))
            self.url = info.baseInfo.imgUrl
            self.path = ""
            self.idLabel.setText("https://{}.org/g/{}/{}".format(self.site, self.bookId, self.token))
            self.updateTick.setText(info.pageInfo.posted)
            self.favoriteLabel.setText(str(info.pageInfo.favorites))
            self.pageLabel.setText(str(info.pageInfo.pages))
            self.lanLabel.setText(info.pageInfo.language)
            self.categoryList.clear()
            self.categoryList.AddItem(info.baseInfo.category)
            self.commentButton.setText("({})".format(len(info.pageInfo.comment)))
            self.SetTagInfo(info.baseInfo.tags)
            # for tag in info.baseInfo.tags:
            #     tagData = tag.split(":")
            #     if len(tagData) >= 2:
            #         tagName = tagData[0]
            #         if not tagName:
            #             tag = "misc" + tag
            #
            #     label = QLabel(tag)
            #     label.setAlignment(Qt.AlignCenter)
            #     label.setStyleSheet("color: rgb(196, 95, 125);")
            #     font = QFont()
            #     font.setPointSize(12)
            #     font.setBold(True)
            #     label.setFont(font)

                # item = QListWidgetItem(self.epsListWidget)
                # item.setSizeHint(label.sizeHint() + QSize(20, 20))

                # tagData = tag.split(":")
                # if Setting.Language.autoValue != 3:
                #     if len(tagData) >= 2:
                #         tagName = tagData[0]
                #         if tagName in self.tags:
                #             if tagData[1] in self.tags.get(tagName, {}).get("data"):
                #                 tagInfo = self.tags.get(tagName, {}).get("data", {}).get(tagData[1], {})
                #                 label.setText(self.tags.get(tagName, {}).get("name", "") + ":" + tagInfo.get("dest", ""))
                #                 item.setToolTip(tagInfo.get('description', ""))
                #
                # # item.setToolTip(epsInfo.title)
                # self.epsListWidget.setItemWidget(item, label)
                # self.nameToTag[label.text()] = tag

            if config.IsLoadingPicture:
                self.AddDownloadTask(self.url, self.GetCoverKey(self.bookId, self.token, config.CurSite), completeCallBack=self.UpdatePicture, isReload=True)
            self.preListWidget.UpdatePage(1, maxPages)
            self.preListWidget.UpdateState()
            for index in range(1, 21):
                if index in info.pageInfo.preUrl:
                    self.preListWidget.AddPicutreItem(self.bookId, self.token, str(index), info.pageInfo.preUrl[index])
                else:
                    break

            self.lastEpsId = -1
            self.LoadHistory()
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
            radio = self.devicePixelRatioF()
            pic.setDevicePixelRatio(radio)
            newPic = pic.scaled(self.picture.size()*radio, QtCore.Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.picture.setPixmap(newPic)
            # self.picture.setScaledContents(True)
            self.update()
        else:
            self.picture.setText(Str.GetStr(Str.LoadingFail))
        return

    def LoadNextPage(self):
        page = self.preListWidget.page+1
        maxPage = self.preListWidget.pages
        if page > maxPage:
            return
        start = (page-1) * 20+1
        end = page * 20 + 1
        info = BookMgr().GetBookBySite(self.bookId, self.site)
        if not info:
            return

        if start not in info.pageInfo.preUrl:
            QtOwner().ShowLoading()
            self.AddHttpTask(req.BookInfoReq(self.bookId, token=self.token, site=self.site, page=page), self.LoadNextPageBack)
            return
        self.preListWidget.UpdateState()
        for index in range(start, end):
            if index in info.pageInfo.preUrl:
                self.preListWidget.AddPicutreItem(self.bookId, self.token, str(index), info.pageInfo.preUrl[index])
            else:
                break
        return

    def LoadNextPageBack(self, raw):
        QtOwner().CloseLoading()
        self.preListWidget.UpdateState()
        st = raw["st"]
        if st == Status.Ok:
            page = self.preListWidget.page+1
            self.preListWidget.UpdatePage(self.preListWidget.page+1, self.preListWidget.pages)
            info = BookMgr().GetBookBySite(self.bookId, self.site)
            if not info:
                return
            start = (page - 1) * 20+1
            end = page * 20 + 1
            for index in range(start, end):
                if index in info.pageInfo.preUrl:
                    self.preListWidget.AddPicutreItem(self.bookId, self.token, str(index), info.pageInfo.preUrl[index])
                else:
                    break

    def StartRead(self):
        QtOwner().OpenReadView(self.bookId, self.token, self.site, self.title.text(), self.lastIndex)
        return

    def StartReadIndex(self, index):
        QtOwner().OpenReadView(self.bookId, self.token, self.site, self.title.text(), index)
        return

    def LoadHistory(self):
        info = QtOwner().historyView.GetHistory(self.bookId)
        if not info:
            self.startRead.setText(Str.GetStr(Str.LookFirst))
            self.lastIndex = 0
            return
        self.lastIndex = info.picIndex
        self.startRead.setText(Str.GetStr(Str.LastLook) + str(info.picIndex + 1) + Str.GetStr(Str.Page))
        return

    def ClickTagsItem(self, text):
        # widget = self.epsListWidget.itemWidget(item)
        # text = self.nameToTag.get(widget.text())
        data = text.split("|")
        if data[0]:
            text = data[0]
        text = text.strip("|").strip("$")
        text2 = text.split(":")
        if len(text2) >= 2:
            newText = text2[0] + ":\"" + text2[1] + "$\""
        else:
            newText = text+"$"

        QtOwner().OpenSearch2(newText)
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

    def SetTagInfo(self, tagInfo):
        newTagData = {}
        # self.tagScrollArea.setStyleSheet("")
        for tag in tagInfo:
            tagData = tag.split(":")
            if len(tagData) >= 2:
                tagName = tagData[0]
                if not tagName:
                    tagName = "misc"
                    tag = "misc" + tag
            else:
                continue
            tagList = newTagData.setdefault(tagName, [])
            if Setting.Language.autoValue != 3:
                if tagName in self.tags:
                    if tagData[1] in self.tags.get(tagName.lower(), {}).get("data"):
                        tagInfo = self.tags.get(tagName.lower(), {}).get("data", {}).get(tagData[1], {})
                        tagList.append((tag, self.tags.get(tagName.lower(), {}).get("name", "") + ":" + tagInfo.get("dest", ""), tagInfo.get('description', "")))
                        continue
            tagList.append((tag, tag, ""))

        # item.setToolTip(epsInfo.title)
        # for i in reversed(range(self.verticalLayout.count())):
        #     self.verticalLayout.itemAt(i).widget().setParent(None)
        # self.verticalLayout.setParent(None)
        # self.verticalLayout = QVBoxLayout(self.tagWidgetContents)
        for i in self.allFlowLayout:
            for j in reversed(range(i.count())):
                i.itemAt(j).widget().setParent(None)

            self.verticalLayout.removeItem(i)
            i.setParent(None)
        for i in self.allFlowLabel:
            self.verticalLayout.removeWidget(i)
            i.setParent(None)

        self.allFlowLabel = []
        self.allFlowLayout = []
        if self.flowHorizontalSpacer:
            self.verticalLayout.removeItem(self.flowHorizontalSpacer)
            self.flowHorizontalSpacer = None

        for title, contentList in newTagData.items():
            if Setting.Language.autoValue != 3:
                if title in self.tags:
                    title = self.tags.get(title).get("name", "")
            label = QLabel(title)
            self.verticalLayout.addWidget(label)
            self.allFlowLabel.append(label)
            layout = FlowLayout()
            for tag, text, desc in contentList:
                box = QPushButton(text)
                box.clicked.connect(partial(self.ClickTagsItem, tag))
                box.setMinimumWidth(160)
                box.setToolTip(desc)
                layout.addWidget(box)
            self.verticalLayout.addLayout(layout)
            self.allFlowLayout.append(layout)
        self.flowHorizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.flowHorizontalSpacer)
        return