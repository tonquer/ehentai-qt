from enum import Enum
from functools import partial

from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QEvent, QSize
from PySide2.QtGui import QPixmap, QImage, QCursor
from PySide2.QtWidgets import QDesktopWidget, QMenu

from conf import config
from src.book.book import BookMgr
from src.qt.com.qtloading import QtLoading
from src.qt.qt_main import QtOwner
from src.qt.read.qtreadimg_frame import QtImgFrame
from src.qt.struct.qt_define import QtFileData
from src.qt.util.qttask import QtTaskBase
from src.server import req
from src.util import ToolUtil, Log
from src.util.status import Status
from src.util.tool import time_me


class ReadMode(Enum):
    """ 阅读模式 """
    UpDown = 0              # 上下模式
    LeftRight = 1           # 默认
    LeftRightDouble = 2     # 左右双页
    RightLeftDouble = 3     # 右左双页
    LeftRightScroll = 4     # 左右滚动
    RightLeftScroll = 5     # 右左滚动


class QtReadImg(QtWidgets.QWidget, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.loadingForm = QtLoading(self)
        QtTaskBase.__init__(self)
        self.bookId = ""
        self.epsId = 0
        self.resetCnt = config.ResetCnt
        self.curIndex = 0

        self.pictureData = {}
        self.maxPic = 0

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QtImgFrame(self)

        self.gridLayout.addWidget(self.frame)
        self.setMinimumSize(300, 300)
        self.stripModel = ReadMode(config.LookReadMode)
        self.isStripModel = True
        self.setWindowFlags(self.windowFlags() & ~ Qt.WindowMaximizeButtonHint & ~ Qt.WindowMinimizeButtonHint)

        ToolUtil.SetIcon(self)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.SelectMenu)

        self.category = []
        self.isInit = False
        self.epsName = ""

    def LoadSetting(self):
        self.stripModel = ReadMode(config.LookReadMode)
        self.ChangeReadMode(config.LookReadMode)
        return

    def SelectMenu(self):
        popMenu = QMenu(self)
        action = popMenu.addAction(self.tr("菜单"))
        action.triggered.connect(self.ShowAndCloseTool)

        action = popMenu.addAction(self.tr("全屏切换"))
        action.triggered.connect(self.qtTool.FullScreen)

        menu2 = popMenu.addMenu(self.tr("阅读模式"))

        def AddReadMode(name, value):
            action = menu2.addAction(name)
            action.triggered.connect(partial(self.ChangeReadMode, value))
            if self.stripModel.value == value:
                action.setCheckable(True)
                action.setChecked(True)
        AddReadMode(self.tr("上下滚动"), 0)
        AddReadMode(self.tr("默认"), 1)
        AddReadMode(self.tr("左右双页"), 2)
        AddReadMode(self.tr("右左双页"), 3)
        AddReadMode(self.tr("左右滚动"), 4)
        AddReadMode(self.tr("右左滚动"), 5)

        menu3 = popMenu.addMenu(self.tr("缩放"))

        def AddScaleMode(name, value):
            action = menu3.addAction(name)
            action.triggered.connect(partial(self.qtTool.ScalePicture, value))
            if (self.frame.scaleCnt+10) * 10 == value:
                action.setCheckable(True)
                action.setChecked(True)
        AddScaleMode("50%", 50)
        AddScaleMode("60%", 60)
        AddScaleMode("70%", 70)
        AddScaleMode("80%", 80)
        AddScaleMode("90%", 90)
        AddScaleMode("100%", 100)
        AddScaleMode("120%", 120)
        AddScaleMode("140%", 140)
        AddScaleMode("160%", 160)
        AddScaleMode("180%", 180)
        AddScaleMode("200%", 200)

        action = popMenu.addAction(self.tr("退出"))
        action.triggered.connect(self.close)
        popMenu.exec_(QCursor.pos())

    @property
    def graphicsView(self):
        return self.frame.graphicsView

    @property
    def graphicsGroup(self):
        return self.frame.graphicsGroup

    @property
    def qtTool(self):
        return self.frame.qtTool

    def closeEvent(self, a0) -> None:
        self.ReturnPage()
        QtOwner().owner.bookInfoForm.show()
        self.Clear()
        a0.accept()

    def Clear(self):
        self.qtTool.UpdateText("")
        self.frame.UpdateProcessBar(None)
        self.bookId = ""
        self.epsId = 0
        self.maxPic = 0
        self.curIndex = 0
        # if self.stripModel != ReadMode.UpDown:
        #     self.qtTool.zoomSlider.setValue(100)
        #     self.frame.scaleCnt = 0
        # else:
        #     self.qtTool.zoomSlider.setValue(120)
        #     self.frame.scaleCnt = 2
        self.frame.oldValue = 0
        self.pictureData.clear()
        self.ClearTask()
        self.ClearConvert()
        self.ClearQImageTask()

    def OpenPage(self, bookId, name):
        if not bookId:
            return
        self.Clear()
        self.bookId = bookId
        self.CheckGetBookPage()
        self.qtTool.checkBox.setChecked(config.IsOpenWaifu)
        self.qtTool.SetData(isInit=True)
        # self.graphicsGroup.setPixmap(QPixmap())
        self.frame.InitPixMap()
        self.frame.UpdatePixMap()
        self.qtTool.SetData()
        # self.qtTool.show()
        self.AddHistory()

        if not self.isInit:
            desktop = QDesktopWidget()
            self.resize(desktop.width() // 4 * 3, desktop.height() - 100)
            self.move(desktop.width() // 8, 0)
            self.isInit = True
        # historyInfo = self.owner().historyForm.GetHistory(bookId)
        # if historyInfo and historyInfo.epsId == epsId:
        #     self.curIndex = historyInfo.picIndex
        # else:
        #     self.AddHistory()
        # self.AddHistory()
        self.epsName = name
        self.loadingForm.show()
        self.StartLoadPicUrl()
        self.setWindowTitle(self.epsName)
        self.show()

        if config.LookReadFull:
            self.showFullScreen()
            self.qtTool.fullButton.setText(self.tr("退出全屏"))
        else:
            self.showNormal()
            self.qtTool.fullButton.setText(self.tr("全屏"))

        if config.IsTips:
            config.IsTips = 0
            self.frame.InitHelp()

    def ReturnPage(self):
        self.AddHistory()
        QtOwner().owner.bookInfoForm.LoadHistory()
        return

    def CheckLoadPicture(self):
        # i = 0
        newDict = {}
        needUp = False
        removeTaskIds = []

        preLoadList = list(range(self.curIndex, self.curIndex + config.PreLoading))

        # 预加载上一页
        if len(preLoadList) >= 2 and self.curIndex > 0:
            preLoadList.insert(2, self.curIndex - 1)

        for i, p in self.pictureData.items():
            if i in preLoadList:
                newDict[i] = p
            else:
                needUp = True
                if p.waifu2xTaskId > 0:
                    removeTaskIds.append(p.waifu2xTaskId)

        if needUp:
            self.pictureData.clear()
            self.pictureData = newDict
            self.ClearWaitConvertIds(removeTaskIds)

        for i in preLoadList:
            if i >= self.maxPic or i < 0:
                continue

            bookInfo = BookMgr().GetBook(self.bookId)
            p = self.pictureData.get(i)
            if not p:
                imgUrl = bookInfo.pageInfo.picRealUrl.get(i + 1)
                if imgUrl:
                    self.AddDownload(i, imgUrl)
                else:
                    self.GetPictureUrl(i)
                break
            elif p.state == p.Downloading or p.state == p.DownloadReset:
                break

        for i in preLoadList:
            if i >= self.maxPic or i < 0:
                continue
            if config.IsOpenWaifu:
                p = self.pictureData.get(i)
                if not p or not p.data:
                    break
                if p.waifuState == p.WaifuStateCancle or p.waifuState == p.WaifuWait:
                    p.waifuState = p.WaifuStateStart
                    bookInfo = BookMgr().GetBook(self.bookId)
                    imgUrl = bookInfo.pageInfo.picRealUrl.get(i + 1)
                    self.AddCovertData(imgUrl, i)
                    break
                if p.waifuState == p.WaifuStateStart:
                    break
        pass

    def StartLoadPicUrl(self):
        bookInfo = BookMgr().GetBook(self.bookId)
        self.maxPic = bookInfo.pageInfo.pages
        self.CheckLoadPicture()
        self.qtTool.InitSlider(self.maxPic)
        return

    def UpdateProcessBar(self, data, laveFileSize, backParam):
        info = self.pictureData.get(backParam)
        if not info:
            return
        if laveFileSize < 0:
            info.downloadSize = 0
        if info.size <= 0:
            info.size = laveFileSize
        info.downloadSize += len(data)
        if self.curIndex != backParam:
            return
        self.frame.UpdateProcessBar(info)

    def CompleteDownloadPic(self, data, st, index):
        self.loadingForm.close()
        p = self.pictureData.get(index)
        if not p:
            p = QtFileData()
            self.pictureData[index] = p
        bookInfo = BookMgr().GetBook(self.bookId)
        if st != Status.Ok:
            p.state = p.DownloadReset
            self.AddDownload(index, bookInfo.pageInfo.picRealUrl.get(index+1))
        else:
            p.SetData(data, self.category)
            self.AddQImageTask(data, self.ConvertQImageBack, index)
            self.CheckLoadPicture()
            # if index == self.curIndex:
            #     self.ShowImg()
            # elif self.isStripModel and self.curIndex < index <= self.curIndex + 2:
            #     self.ShowOtherPage()
            #     self.CheckLoadPicture()
            # else:
            #     self.CheckLoadPicture()
            # return

    @time_me
    def ShowOtherPage(self, isShowWaifu=True):
        for index in range(self.curIndex+1, self.curIndex+3):
            p = self.pictureData.get(index)
            if not p or (not p.data) or (not p.cacheImage):
                self.frame.SetPixIem(index-self.curIndex, QPixmap())
                continue

            assert isinstance(p, QtFileData)
            if not isShowWaifu:
                p2 = p.cacheImage

            elif p.cacheWaifu2xImage:
                p2 = p.cacheWaifu2xImage
            else:
                p2 = p.cacheImage

            pixMap = QPixmap(p2)
            self.frame.SetPixIem(index-self.curIndex, pixMap)
        # self.frame.ScalePicture()
        return True

    @time_me
    def ShowImg(self, isShowWaifu=True):
        p = self.pictureData.get(self.curIndex)

        if not p or (not p.data) or (not p.cacheImage):
            if not p or (not p.data):
                self.qtTool.SetData(state=QtFileData.Downloading)
            else:
                self.qtTool.SetData(state=QtFileData.Converting)

            self.frame.SetPixIem(0, QPixmap())

            self.qtTool.modelBox.setEnabled(False)
            self.frame.UpdateProcessBar(None)
            self.frame.process.show()
            return

        self.frame.process.hide()
        if config.CanWaifu2x:
            self.qtTool.modelBox.setEnabled(True)
        assert isinstance(p, QtFileData)
        if not isShowWaifu:
            self.frame.waifu2xProcess.hide()
            self.qtTool.SetData(waifuSize=QSize(0, 0), waifuDataLen=0)
            p2 = p.cacheImage

        elif p.cacheWaifu2xImage:
            p2 = p.cacheWaifu2xImage
            self.frame.waifu2xProcess.hide()
            self.qtTool.SetData(waifuSize=p.waifuQSize, waifuDataLen=p.waifuDataSize,
                                waifuTick=p.waifuTick)

        else:
            p2 = p.cacheImage
            if config.IsOpenWaifu:
                self.frame.waifu2xProcess.show()
            else:
                self.frame.waifu2xProcess.hide()

        self.qtTool.SetData(pSize=p.qSize, dataLen=p.size, state=p.state, waifuState=p.waifuState)
        self.qtTool.UpdateText(p.model)

        pixMap = QPixmap(p2)
        self.frame.SetPixIem(0, pixMap)
        # self.graphicsView.setSceneRect(QRectF(QPointF(0, 0), QPointF(pixMap.width(), pixMap.height())))
        # self.frame.ScalePicture()
        self.CheckLoadPicture()
        return True

    def eventFilter(self, obj, ev):
        if ev.type() == QEvent.KeyPress:
            return True
        else:
            return super(self.__class__, self).eventFilter(obj, ev)

    def zoomIn(self):
        """放大"""
        self.zoom(1.1)

    def zoomOut(self):
        """缩小"""
        self.zoom(1/1.1)

    def zoom(self, scaleV):
        """缩放
        :param factor: 缩放的比例因子
        """
        # q = QMatrix()
        # q.setMatrix(1, self.graphicsView.matrix().m12(), self.graphicsView.matrix().m21(), 1, self.graphicsView.matrix().dx(), self.graphicsView.matrix().dy())
        # self.graphicsView.setMatrix(q, False)

        # _factor = self.graphicsView.transform().scale(
        #     factor, factor).mapRect(QRectF(0, 0, 1, 1)).width()
        # print(_factor)
        # if _factor < 0.07 or _factor > 100:
        #     # 防止过大过小
        #     return
        if self.frame.scaleCnt == scaleV:
            return
        # for _ in range(abs(scaleV - self.frame.scaleCnt)):
        #     if scaleV - self.frame.scaleCnt > 0:
        #         self.graphicsView.scale(1.1, 1.1)
        #     else:
        #         self.graphicsView.scale(1/1.1, 1/1.1)
        self.frame.scaleCnt = scaleV
        self.frame.ScalePicture()

    def keyReleaseEvent(self, ev):
        # print(ev.modifiers, ev.key())
        if ev.key() == Qt.Key_Plus or ev.key() == Qt.Key_Equal:
            self.qtTool.zoomSlider.setValue(self.qtTool.zoomSlider.value()+10)
            return True
        if ev.key() == Qt.Key_Minus:
            self.qtTool.zoomSlider.setValue(self.qtTool.zoomSlider.value()-10)
            return True
        if ev.key() == Qt.Key_Escape:
            # if self.windowState() == Qt.WindowFullScreen:
            #     self.showNormal()
            #     self.frame.qtTool.fullButton.setText("全屏")
            #     return
            self.qtTool.ReturnPage()
            return True
        # elif ev.key() == Qt.Key_Up:
        #     point = self.graphicsItem.pos()
        #     self.graphicsItem.setPos(point.x(), point.y()+50)
        #     return
        # elif ev.key() == Qt.Key_Down:
        #     point = self.graphicsItem.pos()
        #     self.graphicsItem.setPos(point.x(), point.y()-50)
        #     return
        return super(self.__class__, self).keyReleaseEvent(ev)

    def AddHistory(self):
        # bookName = QtOwner().owner.bookInfoForm.bookName
        # url = QtOwner().owner.bookInfoForm.url
        # path = QtOwner().owner.bookInfoForm.path
        # QtOwner().owner.historyForm.AddHistory(self.bookId, bookName, self.epsId, self.curIndex, url, path)
        return

    def ShowAndCloseTool(self):
        if self.qtTool.isHidden():
            self.qtTool.show()
        else:
            self.qtTool.hide()

    def Waifu2xBack(self, data, waifu2xId, index, tick):
        p = self.pictureData.get(index)
        if waifu2xId <= 0 or not p:
            Log.Error("Not found waifu2xId ：{}, index: {}".format(str(waifu2xId), str(index)))
            return
        p.SetWaifuData(data, round(tick, 2))
        self.AddQImageTask(data, self.ConvertQImageWaifu2xBack, index)
        self.CheckLoadPicture()
        # if index == self.curIndex:
        #     self.qtTool.SetData(waifuState=p.waifuState)
        #     self.ShowImg()
        # elif self.isStripModel and self.curIndex < index <= self.curIndex + 2:
        #     self.ShowOtherPage()
        #     self.CheckLoadPicture()
        # else:
        #     self.CheckLoadPicture()

    def ConvertQImageWaifu2xBack(self, data, index):
        assert isinstance(data, QImage)
        p = self.pictureData.get(index)
        if not p:
            return
        assert isinstance(p, QtFileData)
        p.cacheWaifu2xImage = data
        if index == self.curIndex:
            self.ShowImg()
        elif self.isStripModel and self.curIndex < index <= self.curIndex + 2:
            self.ShowOtherPage()
        return

    def AddCovertData(self, imgUrl, i):
        info = self.pictureData[i]
        if not info and info.data:
            return
        assert isinstance(info, QtFileData)
        path = "{}/{}/{}".format(config.CurSite, self.bookId, i)
        info.waifu2xTaskId = self.AddConvertTask(path, info.data, info.model, self.Waifu2xBack, i)
        if i == self.curIndex:
            self.qtTool.SetData(waifuState=info.waifuState)
            self.frame.waifu2xProcess.show()

    def AddDownload(self, i, imgUrl):
        path = QtOwner().owner.downloadForm.GetDonwloadFilePath(self.bookId, i)
        self.AddDownloadTask(imgUrl, "{}/{}/{}".format(config.CurSite, self.bookId, i),
                                 downloadCallBack=self.UpdateProcessBar,
                                 completeCallBack=self.CompleteDownloadPic, backParam=i,
                                 isSaveCache=True, filePath=path)
        if i not in self.pictureData:
            data = QtFileData()
            self.pictureData[i] = data
        self.qtTool.SetData(state=self.pictureData[i].state)

    def GetPictureUrl(self, i):
        info = BookMgr().GetBook(self.bookId)
        if not info.pageInfo.GetImgKey(i):
            Log.Warn("Not found picture url, {}:{}".format(info.baseInfo.id, i))
            return
        QtOwner().SetDirty()
        self.AddHttpTask(req.GetBookImgUrl2(self.bookId, i+1), self.GetPictureUrlBack, i)

    def GetPictureUrlBack(self, msg, i):
        self.CheckLoadPicture()

    def CheckGetBookPage(self):
        info = BookMgr().GetBook(self.bookId)
        if info.curPage >= info.maxPage:
            return
        QtOwner().SetDirty()
        self.AddHttpTask(req.BookInfoReq(self.bookId, info.curPage+1), self.GetBookPageBack)

    def GetBookPageBack(self, data):
        self.CheckGetBookPage()
        self.CheckLoadPicture()

    def ConvertQImageBack(self, data, index):
        assert isinstance(data, QImage)
        p = self.pictureData.get(index)
        if not p:
            return
        assert isinstance(p, QtFileData)
        p.cacheImage = data
        if index == self.curIndex:
            self.ShowImg()
        elif self.isStripModel and self.curIndex < index <= self.curIndex + 2:
            self.ShowOtherPage()
        return

    def ChangeReadMode(self, index):
        self.qtTool.comboBox.setCurrentIndex(index)