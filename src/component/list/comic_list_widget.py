from functools import partial

from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QListWidgetItem, QMenu, QApplication

from component.list.base_list_widget import BaseListWidget
from component.widget.comic_item_widget import ComicItemWidget
from config import config
from config.setting import Setting
from qt_owner import QtOwner
from tools.book import BookMgr
from tools.status import Status
from tools.str import Str
from tools.tool import ToolUtil


class ComicListWidget(BaseListWidget):
    def __init__(self, parent):
        BaseListWidget.__init__(self, parent)
        self.resize(800, 600)
        # self.setMinimumHeight(400)
        self.setFrameShape(self.Shape.NoFrame)  # 无边框
        self.setFlow(self.Flow.LeftToRight)  # 从左到右
        self.setWrapping(True)
        self.setResizeMode(self.ResizeMode.Adjust)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.SelectMenuBook)
        # self.doubleClicked.connect(self.OpenBookInfo)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.itemClicked.connect(self.SelectItem)
        self.nextId = ""
        self.isDelMenu = False
        self.isGame = False
        self.isLocal = False
        self.isLocalEps = False
        self.isMoveMenu = False
        self.openMenu = False

    def SelectMenuBook(self, pos):
        index = self.indexAt(pos)
        widget = self.indexWidget(index)
        if index.isValid() and widget:
            popMenu = QMenu(self)
            if not self.isLocal:
                action = popMenu.addAction(Str.GetStr(Str.Open))
                action.triggered.connect(partial(self.OpenBookInfoHandler, index))
            action = popMenu.addAction(Str.GetStr(Str.LookCover))
            action.triggered.connect(partial(self.OpenPicture, index))
            action = popMenu.addAction(Str.GetStr(Str.ReDownloadCover))
            action.triggered.connect(partial(self.ReDownloadPicture, index))
            if config.CanWaifu2x and widget.picData:
                if not widget.isWaifu2x:
                    action = popMenu.addAction(Str.GetStr(Str.Waifu2xConvert))
                    action.triggered.connect(partial(self.Waifu2xPicture, index))
                    if widget.isWaifu2xLoading or not config.CanWaifu2x:
                        action.setEnabled(False)
                else:
                    action = popMenu.addAction(Str.GetStr(Str.DelWaifu2xConvert))
                    action.triggered.connect(partial(self.CancleWaifu2xPicture, index))
            action = popMenu.addAction(Str.GetStr(Str.CopyTitle))
            action.triggered.connect(partial(self.CopyHandler, index))
            if not self.isLocal:
                action = popMenu.addAction(Str.GetStr(Str.Download))
                action.triggered.connect(partial(self.DownloadHandler, index))
            if self.isDelMenu:
                action = popMenu.addAction(Str.GetStr(Str.Delete))
                action.triggered.connect(partial(self.DelHandler, index))
            if self.isMoveMenu:

                action = popMenu.addAction(Str.GetStr(Str.Move))
                action.triggered.connect(partial(self.MoveHandler, index))
            if self.openMenu:
                action = popMenu.addAction(Str.GetStr(Str.OpenDir))
                action.triggered.connect(partial(self.OpenDirHandler, index))
            popMenu.exec_(QCursor.pos())
        return

    # def AddBookByDict(self, v):
    #     _id = v.get("_id")
    #     title = v.get("title")
    #     categories = v.get("categories", [])
    #     if "thumb" in v:
    #         url = v.get("thumb", {}).get("fileServer")
    #         path = v.get("thumb", {}).get("path")
    #     elif "icon" in v:
    #         url = v.get("icon", {}).get("fileServer")
    #         path = v.get("icon", {}).get("path")
    #     else:
    #         url = ""
    #         path = ""
    #     categoryStr = "，".join(categories)
    #     likesCount = str(v.get("totalLikes", ""))
    #     finished = v.get("finished")
    #     pagesCount = v.get("pagesCount")
    #     self.AddBookItem(_id, title, categoryStr, url, path, likesCount, "", pagesCount, finished)

    def AddBookByLocal(self, v, category=""):
        from task.task_local import LocalData
        assert isinstance(v, LocalData)
        index = self.count()
        widget = ComicItemWidget()
        widget.setFocusPolicy(Qt.NoFocus)
        widget.id = v.id
        title = v.title
        widget.index = index
        widget.title = v.title
        widget.picNum = v.picCnt
        widget.url = v.file
        if len(v.eps) > 0:
            title += "<font color=#d5577c>{}</font>".format("(" + str(len(v.eps)) + "E)")
        else:
            title += "<font color=#d5577c>{}</font>".format("(" + str(v.picCnt) + "P)")
        if v.lastReadTime:
            categories = "{} {}".format(ToolUtil.GetUpdateStrByTick(v.lastReadTime), Str.GetStr(Str.Looked))

            widget.timeLabel.setText(categories)
        else:
            widget.timeLabel.setVisible(False)
            widget.starButton.setVisible(False)

        widget.categoryLabel.setVisible(False)
        if category:
            widget.categoryLabel.setText(category)
            widget.categoryLabel.setVisible(True)

        widget.nameLable.setText(title)
        item = QListWidgetItem(self)
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        item.setSizeHint(widget.sizeHint())
        self.setItemWidget(item, widget)
        widget.picLabel.setText(Str.GetStr(Str.LoadingPicture))
        widget.PicLoad.connect(self.LoadingPicture)

    # def AddBookItemByBook(self, v, isShowHistory=False):
    #     title = v.title
    #     url = v.fileServer
    #     path = v.path
    #     _id = v.id
    #     finished = v.finished
    #     pagesCount = v.pages
    #     likesCount = str(v.likesCount)
    #     updated_at = v.updated_at
    #     categories = v.categories
    #     updated_at = v.updated_at
    #     if isShowHistory:
    #         info = QtOwner().owner.historyView.GetHistory(_id)
    #         if info:
    #             categories = Str.GetStr(Str.LastLook) + str(info.epsId + 1) + Str.GetStr(Str.Chapter) + "/" + str(v.epsCount) + Str.GetStr(Str.Chapter)
    #     self.AddBookItem(_id, title, categories, url, path, likesCount, updated_at, pagesCount, finished)

    def AddBookItemByHistory(self, v):
        _id = v.bookId
        token = v.token
        title = v.name
        url = v.url
        categories = "{} {}".format(ToolUtil.GetUpdateStrByTick(v.tick), Str.GetStr(Str.Looked))
        self.AddBookItem(_id, title, categories, url, "", token=token)

    def AddBookItem(self, _id, title, categoryStr="", url="", path="", likesCount="", updated_at="", pagesCount="", finished="", token=""):
        index = self.count()
        widget = ComicItemWidget()
        widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        widget.id = _id
        widget.token = token
        widget.url = url
        widget.path = path
        widget.index = index
        widget.categoryLabel.setText(categoryStr)
        widget.nameLable.setText(title)
        if updated_at:
            dayStr = ToolUtil.GetUpdateStr(updated_at)
            updateStr = dayStr + Str.GetStr(Str.Update)
            widget.timeLabel.setText(updateStr)
            widget.timeLabel.setVisible(True)
        else:
            widget.timeLabel.setVisible(False)

        if likesCount:
            widget.starButton.setText(str(likesCount))
            widget.starButton.setVisible(True)
        else:
            widget.starButton.setVisible(False)

        if pagesCount:
            title += "<font color=#d5577c>{}</font>".format("("+str(pagesCount)+"P)")
        if finished:
            title += "<font color=#d5577c>{}</font>".format("({})".format(Str.GetStr(Str.ComicFinished)))

        item = QListWidgetItem(self)
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        item.setSizeHint(widget.sizeHint())
        self.setItemWidget(item, widget)
        widget.picLabel.setText(Str.GetStr(Str.LoadingPicture))
        widget.PicLoad.connect(self.LoadingPicture)

    def AddPicutreItem(self, bookId, token, name, url):
        index = self.count()
        widget = ComicItemWidget()
        widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        widget.url = url
        widget.id = bookId
        widget.token = token
        widget.index = index
        widget.isPicture = True
        widget.categoryLabel.setVisible(False)
        widget.nameLable.setText(name)
        widget.timeLabel.setVisible(False)
        widget.starButton.setVisible(False)

        item = QListWidgetItem(self)
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        item.setSizeHint(widget.sizeHint())
        self.setItemWidget(item, widget)
        widget.picLabel.setText(Str.GetStr(Str.LoadingPicture))
        widget.PicLoad.connect(self.LoadingPicture)

    def LoadingPicture(self, index):
        item = self.item(index)
        widget = self.itemWidget(item)
        assert isinstance(widget, ComicItemWidget)
        if not widget.isPicture:
            key = self.GetCoverKey(widget.id, widget.token, config.CurSite)
        else:
            key = self.GetPreCoverKey(widget.id, widget.token, config.CurSite, index+1)
        self.AddDownloadTask(widget.url, key, completeCallBack=self.LoadingPictureComplete, backParam=index)

    def LoadingPictureComplete(self, data, status, index):
        if status == Status.Ok:
            item = self.item(index)
            widget = self.itemWidget(item)
            if not widget:
                return
            widget.SetPicture(data)
            assert isinstance(widget, ComicItemWidget)
            if Setting.CoverIsOpenWaifu.value:
                item = self.item(index)
                indexModel = self.indexFromItem(item)
                self.Waifu2xPicture(indexModel, True)
            pass
        else:
            item = self.item(index)
            widget = self.itemWidget(item)
            if not widget:
                return
            assert isinstance(widget, ComicItemWidget)
            widget.SetPictureErr(status)
        return

    def SelectItem(self, item):
        assert isinstance(item, QListWidgetItem)
        widget = self.itemWidget(item)
        if widget.isPicture:
            QtOwner().StartReadIndex(widget.index)
            return

        if self.isGame:
            QtOwner().OpenGameInfo(widget.id)
        elif self.isLocalEps:
            QtOwner().OpenLocalEpsBook(widget.id)
        elif self.isLocal:
            QtOwner().OpenLocalBook(widget.id)
        else:

            QtOwner().OpenBookInfo(widget.id, widget.token)
        return

    def OpenBookInfoHandler(self, index):
        widget = self.indexWidget(index)
        if widget:
            QtOwner().OpenBookInfo(widget.id)
            return

    def OpenPicture(self, index):
        widget = self.indexWidget(index)
        if widget:
            QtOwner().OpenWaifu2xTool(widget.picData)
            return

    def ReDownloadPicture(self, index):
        widget = self.indexWidget(index)
        if widget:
            if widget.url and config.IsLoadingPicture:
                widget.SetPicture("")
                item = self.itemFromIndex(index)
                count = self.row(item)
                widget.picLabel.setText(Str.GetStr(Str.LoadingPicture))
                self.AddDownloadTask(widget.url, self.GetCoverKey(widget.id, widget.token, config.CurSite), completeCallBack=self.LoadingPictureComplete, backParam=count, isReload=True)
                pass

    def Waifu2xPicture(self, index, isIfSize=False):
        widget = self.indexWidget(index)
        if widget and widget.picData:
            w, h, mat, _ = ToolUtil.GetPictureSize(widget.picData)
            if max(w, h) <= Setting.CoverMaxNum.value or not isIfSize:
                model = ToolUtil.GetModelByIndex(Setting.CoverLookNoise.value, Setting.CoverLookScale.value, Setting.CoverLookModel.value, mat)
                widget.isWaifu2xLoading = True
                if self.isLocal:
                    self.AddConvertTask(widget.path, widget.picData, model, self.Waifu2xPictureBack, index, noSaveCache=True)
                else:
                    self.AddConvertTask(widget.path, widget.picData, model, self.Waifu2xPictureBack, backParam=index)

    def CancleWaifu2xPicture(self, index):
        widget = self.indexWidget(index)
        if widget.isWaifu2x and widget.picData:
            widget.SetPicture(widget.picData)

    def Waifu2xPictureBack(self, data, waifuId, index, tick):
        widget = self.indexWidget(index)
        if data and widget:
            widget.SetWaifu2xData(data)
        return

    def CopyHandler(self, index):
        widget = self.indexWidget(index)
        if widget:
            data = widget.GetTitle() + str("\r\n")
            clipboard = QApplication.clipboard()
            data = data.strip("\r\n")
            clipboard.setText(data)
        pass

    def DelHandler(self, index):
        widget = self.indexWidget(index)
        if widget:
            self.DelCallBack(widget.id)

    def DelCallBack(self, cfgId):
        return

    def DownloadHandler(self, index):
        widget = self.indexWidget(index)
        if widget:
            bookId = widget.id
            token = widget.token
            QtOwner().downloadView.AddDownload(bookId, token, config.CurSite)
            QtOwner().ShowMsg(Str.GetStr(Str.AddDownload))
        pass

    def MoveHandler(self, index):
        return

    def OpenDirHandler(self, index):
        return