from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt, QSize, QEvent
from PySide2.QtGui import QColor, QFont
from PySide2.QtWidgets import QListWidgetItem, QLabel, QDesktopWidget

from conf import config
from src.book.book import BookMgr
from src.qt.com.qtbubblelabel import QtBubbleLabel
from src.qt.com.qtimg import QtImgMgr
from src.qt.com.qtloading import QtLoading
from src.qt.qt_main import QtOwner
from src.qt.util.qttask import QtTaskBase
from src.server import req, Log
from src.util.status import Status
from ui.bookinfo import Ui_BookInfo


class QtBookInfo(QtWidgets.QWidget, Ui_BookInfo, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_BookInfo.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.loadingForm = QtLoading(self)
        self.bookId = ""
        self.url = ""
        self.path = ""
        self.bookName = ""
        self.lastEpsId = -1
        self.pictureData = None

        self.msgForm = QtBubbleLabel(self)
        self.picture.installEventFilter(self)
        self.title.setWordWrap(True)
        self.title.setTextInteractionFlags(Qt.TextSelectableByMouse)
        # self.epsListWidget.setFlow(self.epsListWidget.LeftToRight)
        self.epsListWidget.setWrapping(True)
        self.epsListWidget.setFrameShape(self.epsListWidget.NoFrame)
        self.epsListWidget.setResizeMode(self.epsListWidget.Adjust)

        self.listWidget.InitUser(self.LoadNextPage)
        self.commentButton.clicked.connect(self.SendComment)
        self.commentButton.setEnabled(False)
        self.tags = QtOwner().owner.tags
        desktop = QDesktopWidget()
        self.resize(desktop.width()//4*1, desktop.height()//4*3)
        self.move(desktop.width()//8*3, desktop.height()//4*1)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.stackedWidget.currentIndex() == 1:
            self.stackedWidget.setCurrentIndex(0)
            QtOwner().owner.qtReadImg.AddHistory()
            self.LoadHistory()
            a0.ignore()
        else:
            a0.accept()

    # def OpenAutor(self):
    #     text = self.autor.text()
    #     self.owner().userForm.listWidget.setCurrentRow(0)
    #     self.owner().searchForm.searchEdit.setText(text)
    #     self.owner().searchForm.Search()
    #     return

    def Clear(self):
        self.stackedWidget.setCurrentIndex(0)
        self.ClearTask()
        self.epsListWidget.clear()
        self.listWidget.clear()

    def OpenBook(self, bookId):
        self.bookId = bookId
        self.setWindowTitle(self.bookId)
        self.setFocus()
        # if self.bookId in self.owner().downloadForm.downloadDict:
        #     self.download.setEnabled(False)
        # else:
        #     self.download.setEnabled(True)

        self.Clear()
        self.show()
        self.loadingForm.show()
        self.AddHttpTask(req.BookInfoReq(bookId), self.OpenBookBack)

    def close(self):
        super(self.__class__, self).close()

    def OpenBookBack(self, data):
        self.loadingForm.close()
        st = data.get("st")
        if st == Status.Ok:
            maxPages = data.get("maxPages")
            self.listWidget.UpdatePage(1, maxPages)
            self.listWidget.UpdateState()
            self.epsListWidget.clear()
            info = BookMgr().GetBook(self.bookId)
            self.title.setText(info.baseInfo.title)
            self.bookName = info.baseInfo.title
            self.picture.setText("图片加载中...")
            self.url = info.baseInfo.imgUrl
            self.path = ""
            self.updateTick.setText(info.pageInfo.posted)
            self.views.setText(str(info.pageInfo.favorites))
            self.likes.setText(str(info.pageInfo.pages))
            for tag in info.baseInfo.tags:
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
                if len(tagData) >= 2:
                    if tagData[0] in self.tags:
                        if tagData[1] in self.tags[tagData[0]].get("data"):
                            tagInfo = self.tags[tagData[0]].get("data").get(tagData[1], {})
                            label.setText(self.tags[tagData[0]].get("name", "") + ":" + tagInfo.get("dest", ""))
                            item.setToolTip(tagInfo.get('description', ""))

                # item.setToolTip(epsInfo.title)
                self.epsListWidget.setItemWidget(item, label)

            if config.IsLoadingPicture:
                self.AddDownloadTask(self.url, "", completeCallBack=self.UpdatePicture)
            self.GetCommnetBack(info.pageInfo.comment)
        else:
            QtBubbleLabel.ShowErrorEx(self, st)
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
            self.picture.setText("图片加载失败")
        return

    # 加载评论
    def GetCommnetBack(self, data):
        try:
            self.listWidget.page = 1
            self.listWidget.pages = 1
            self.tabWidget.setTabText(1, "评论({})".format(str(len(data))))
            for index, v in enumerate(data):
                createdTime, content = v
                self.listWidget.AddUserItem("", 0, 0, content, "", createdTime, index+1, "",
                                            "", "", "", 0)
            return
        except Exception as es:
            Log.Error(es)

    # def AddDownload(self):
    #     self.owner().epsInfoForm.OpenEpsInfo(self.bookId)
        # if self.owner().downloadForm.AddDownload(self.bookId):
        #     QtBubbleLabel.ShowMsgEx(self, "添加下载成功")
        # else:
        #     QtBubbleLabel.ShowMsgEx(self, "已在下载列表")
        # self.download.setEnabled(False)

    # def AddFavority(self):
    #     User().AddAndDelFavorites(self.bookId)
    #     QtBubbleLabel.ShowMsgEx(self, "添加收藏成功")
    #     self.favorites.setEnabled(False)

    def LoadNextPage(self):
        return
        # self.loadingForm.show()
        # QtTask().AddHttpTask(
        #     lambda x: Server().Send(req.GetComments(self.bookId, self.listWidget.page + 1), bakParam=x),
        #     self.GetCommnetBack, cleanFlag=self.closeFlag)
        # return

    def StartRead(self):
        # if self.lastEpsId >= 0:
        #     self.OpenReadIndex(self.lastEpsId)
        # else:
        # self.OpenReadIndex(0)
        self.hide()
        QtOwner().owner.qtReadImg.OpenPage(self.bookId, self.title.text())
        return

    def LoadHistory(self):
        return

    def ClickTagsItem(self, item):
        text = item.text()
        QtOwner().owner.userForm.listWidget.setCurrentRow(1)
        QtOwner().owner.searchForm.searchEdit.setText(text)
        QtOwner().owner.searchForm.Search()
        return

    def SendComment(self):
        return
        # data = self.commentLine.text()
        # if not data:
        #     return
        # self.commentLine.setText("")
        # self.loadingForm.show()
        # QtTask().AddHttpTask(lambda x: Server().Send(req.SendComment(self.bookId, data), bakParam=x), callBack=self.SendCommentBack)

    # def SendCommentBack(self, msg):
    #     try:
    #         data = json.loads(msg)
    #         if data.get("code") == 200:
    #             QtTask().AddHttpTask(lambda x: Server().Send(req.GetComments(self.bookId), bakParam=x),
    #                                             self.GetCommnetBack, cleanFlag=self.closeFlag)
    #         else:
    #             self.loadingForm.close()
    #             QtBubbleLabel.ShowErrorEx(self, data.get("message", "错误"))
    #         self.commentLine.setText("")
    #     except Exception as es:
    #         self.loadingForm.close()
    #         Log.Error(es)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                if self.pictureData:
                    QtImgMgr().ShowImg(self.pictureData)
                return True
            else:
                return False
        else:
            return super(self.__class__, self).eventFilter(obj, event)

    def keyPressEvent(self, ev):
        key = ev.key()
        if Qt.Key_Escape == key:
            self.close()
        return super(self.__class__, self).keyPressEvent(ev)

    def SaveFavorite(self):
        if not QtOwner().owner.userForm.name.text():
            QtBubbleLabel().ShowErrorEx(self, "未登录")
            return
        QtOwner().owner.favoriteInfoForm.OpenFavorite(self.bookId, self.bookName)
        return