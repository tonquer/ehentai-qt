import os
import weakref

from conf import config
from src.book.book import BookMgr, BookInfo
from src.qt.qt_main import QtOwner
from src.qt.util.qttask import QtTaskBase
from src.server import req
from src.util import ToolUtil, Log
from src.util.status import Status


class DownloadInfo(QtTaskBase):
    Success = "下载完成"
    Reading = "获取信息"
    ReadingEps = "获取分页"
    ReadingPicture = "获取下载地址"
    DownloadCover = "正在下载封面"
    Downloading = "正在下载"
    Waiting = "等待中"
    Pause = "暂停"
    Error = "出错了"
    NotFound = "原始文件不存在"

    Converting = "转换中"
    ConvertSuccess = "转换成功"

    def __init__(self, parent):
        QtTaskBase.__init__(self)
        self.bookId = ""         # 书籍id
        self.title = ""          # 标题
        self.savePath = ""       # 保存路径
        self.convertPath = ""    # Waifu2x路径
        self.domain = ""         # 站点
        self.size = 0            # 大小
        self.token = ""          # token

        self.status = self.Waiting      # 状态
        self.tableRow = 0    # 索引

        self._parent = weakref.ref(parent)

        self.convertStatus = self.Waiting
        self.speedStr = ""

        self.picCnt = 0       # 图片数
        self.speedDownloadLen = 0
        self.downloadLen = 0
        self.resetCnt = 0

        self.curPreDownloadIndex = 0
        self.curPreConvertId = 0   # 转换
        self.resetConvertCnt = 0
        self.tick = 0

    @property
    def db(self):
        return self.parent.db

    @property
    def curCoverPath(self):
        savePath = os.path.dirname(self.savePath)
        return os.path.join(savePath, "{}".format("cover.jpg"))

    @property
    def curSavePath(self):
        savePath = self.savePath
        return os.path.join(savePath, "{:04}.{}".format(self.curPreDownloadIndex + 1, "jpg"))

    @property
    def curConvertPath(self):
        savePath = self.convertPath
        return os.path.join(savePath, "{:04}.{}".format(self.curPreConvertId + 1, "jpg"))

    @property
    def curDownloadPic(self):
        if self.status == self.Success:
            return self.maxDownloadPic
        return self.curPreDownloadIndex

    @property
    def maxDownloadPic(self):
        return self.picCnt

    @property
    def curConvertCnt(self):
        if self.convertStatus == self.ConvertSuccess:
            return self.convertCnt
        return self.curPreConvertId

    @property
    def convertCnt(self):
        return self.picCnt

    @property
    def convertTick(self):
        return str(self.tick) + 's'

    @property
    def parent(self):
        return self._parent()

    @property
    def speed(self):
        return self.speedDownloadLen

    @speed.setter
    def speed(self, value):
        self.speedDownloadLen = value

    def SetStatu(self, status):
        self.status = status
        if self.status == self.Success:
            if self in self.parent.downloadingList:
                self.parent.downloadingList.remove(self)
            self.parent.HandlerDownloadList()
            if config.DownloadAuto:
                self.SetConvertStatu(self.Waiting)
                self.parent.AddConvert(self.bookId)
            else:
                self.SetConvertStatu(self.Pause)
            self.parent.HandlerConvertList()

        if status == self.Pause:
            self.PauseDownload()
        self.db.AddDownloadDB(self)
        self.UpdateTableItem()

    def SetConvertStatu(self, status):
        self.convertStatus = status
        if status == self.Pause:
            self.PauseConvert()
        self.parent.HandlerConvertList()
        self.UpdateTableItem()
        self.db.AddDownloadDB(self)

    def UpdateTableItem(self):
        self.parent.UpdateTableItem(self)

    def AddBookPicInfos(self):
        self.SetStatu(DownloadInfo.Reading)
        QtOwner().SetDirty()
        self.AddHttpTask(req.BookInfoReq(self.bookId, token=self.token, site=self.domain), self.AddBookPicInfosBack)

    def AddBookPicInfosBack(self, data):
        if data["st"] != Status.Ok:
            self.resetCnt += 1
            if self.resetCnt >= 5:
                self.SetStatu(DownloadInfo.Error)
                return
            self.AddBookPicInfos()
        else:
            self.resetCnt = 0
            info = BookMgr().GetBookBySite(self.bookId, self.domain)
            self.title = info.baseInfo.title
            if not self.savePath:
                self.savePath = os.path.join(os.path.join(config.SavePath, config.SavePathDir),
                                             ToolUtil.GetCanSaveName(self.title))
                self.savePath = os.path.join(self.savePath, "default")

            if not self.convertPath:
                self.convertPath = os.path.join(os.path.join(config.SavePath, config.SavePathDir),
                                                ToolUtil.GetCanSaveName(self.title))
                self.convertPath = os.path.join(self.convertPath, "waifu2x")
            self.SetStatu(DownloadInfo.ReadingEps)
            self.CheckGetBookPage()

    def CheckGetBookPage(self):
        info = BookMgr().GetBookBySite(self.bookId, self.domain)
        if info.curPage >= info.maxPage:
            return self.StartDownloadCover()
        QtOwner().SetDirty()
        self.AddHttpTask(req.BookInfoReq(self.bookId, info.curPage+1, token=self.token, site=self.domain), self.GetBookPageBack)

    def GetBookPageBack(self, data):
        if data["st"] == Status.Ok:
            self.resetCnt = 0
        else:
            self.resetCnt += 1
            if self.resetCnt >= 5:
                self.SetStatu(DownloadInfo.Error)
                return
        self.CheckGetBookPage()

    def StartDownloadCover(self):
        self.SetStatu(DownloadInfo.DownloadCover)
        bookInfo = BookMgr().GetBookBySite(self.bookId, self.domain)
        if os.path.isfile(self.curCoverPath):
            return self.StartDownload()
        else:
            imgUrl = bookInfo.baseInfo.imgUrl
            if not imgUrl:
                return self.StartDownload()
            self.downloadLen = 0
            self.AddDownloadTask(imgUrl, "",
                                 downloadCallBack=self.AddDownloadBack,
                                 completeCallBack=self.AddDownloadCompleteBack,
                                 backParam=True,
                                 isSaveCache=False)

    def StartDownload(self):
        self.SetStatu(DownloadInfo.Downloading)
        info = BookMgr().GetBookBySite(self.bookId, self.domain)
        assert isinstance(info, BookInfo)
        if self.curPreDownloadIndex >= info.pageInfo.pages:
            self.SetStatu(DownloadInfo.Success)
        else:
            self.UpdateTableItem()
            self.AddDownload()
        return

    def GetPictureUrl(self, i):
        info = BookMgr().GetBookBySite(self.bookId, self.domain)
        if not info.pageInfo.GetImgKey(i):
            Log.Warn("Not found picture url, {}:{}".format(info.baseInfo.id, i))
            return
        QtOwner().SetDirty()
        self.AddHttpTask(req.GetBookImgUrl2(self.bookId, i+1, self.domain), self.GetPictureUrlBack, i)

    def GetPictureUrlBack(self, msg, i):
        if msg["st"] != Status.Ok:
            self.resetCnt += 1
            if self.resetCnt >= 5:
                self.SetStatu(DownloadInfo.Error)
                return
        else:
            self.resetCnt = 0
        self.AddDownload()

    def AddDownload(self):
        bookInfo = BookMgr().GetBookBySite(self.bookId, self.domain)
        self.picCnt = bookInfo.pageInfo.pages

        isDownloadNext = True
        while self.curPreDownloadIndex < bookInfo.pageInfo.pages:
            if os.path.isfile(self.curSavePath):
                self.curPreDownloadIndex += 1
            else:
                imgUrl = bookInfo.pageInfo.picRealUrl.get(self.curPreDownloadIndex + 1)
                if not imgUrl:
                    return self.GetPictureUrl(self.curPreDownloadIndex)
                isDownloadNext = False
                self.downloadLen = 0
                self.AddDownloadTask(imgUrl, "",
                                     downloadCallBack=self.AddDownloadBack,
                                     completeCallBack=self.AddDownloadCompleteBack,
                                     backParam=False,
                                     isSaveCache=False)
                break

        self.UpdateTableItem()
        if isDownloadNext:
            self.StartDownload()

    def AddDownloadBack(self, data, laveFileSize, backParam):
        self.downloadLen += len(data)
        self.speedDownloadLen += len(data)

    def AddDownloadCompleteBack(self, data, msg, isCover):
        if msg != Status.Ok:
            if msg == -500:
                # 可能是图片url过期了
                bookInfo = BookMgr().GetBookBySite(self.bookId, self.domain)
                if bookInfo:
                    if self.curPreDownloadIndex + 1 in bookInfo.pageInfo.picRealUrl:
                        Log.Warn("Del picture url, may be url expired")
                        bookInfo.pageInfo.picRealUrl.pop(self.curPreDownloadIndex + 1)

            self.resetCnt += 1
            if self.resetCnt >= 5:
                self.SetStatu(DownloadInfo.Error)
                return
            if isCover:
                self.StartDownloadCover()
            else:
                self.AddDownload()
        else:
            self.resetCnt = 0
            try:
                if isCover:
                    path = self.curCoverPath
                else:
                    path = self.curSavePath

                savePath = os.path.dirname(path)
                if not os.path.isdir(savePath):
                    os.makedirs(savePath)
                f = open(path, "wb+")
                f.write(data)
                f.close()
                if isCover:
                    self.StartDownload()
                else:
                    self.size += self.downloadLen
                    self.downloadLen = 0
                    self.curPreDownloadIndex += 1
                    self.StartDownload()
            except Exception as es:
                Log.Error(es)
        return

    def StartConvert(self):
        if self.curPreConvertId >= self.picCnt:
            self.SetConvertStatu(self.ConvertSuccess)
        else:
            self.UpdateTableItem()
            self.AddConvert()
        return

    def AddConvert(self):
        savePath = self.savePath
        filePath = os.path.join(savePath, "{:04}.{}".format(self.curPreConvertId + 1, "jpg"))
        if not os.path.isfile(filePath):
            self.status = DownloadInfo.NotFound
            self.SetConvertStatu(self.status)
            return
        isConvertNext = True
        while self.curPreConvertId < self.picCnt:
            if os.path.isfile(self.curConvertPath):
                self.curPreConvertId += 1
            else:
                isConvertNext = False
                f = open(filePath, "rb")
                data = f.read()
                f.close()

                w, h = ToolUtil.GetPictureSize(data)
                model = ToolUtil.GetDownloadScaleModel(w, h)

                self.AddConvertTask("", data, model, self.AddConvertBack)
                break
        self.UpdateTableItem()
        if isConvertNext:
            self.StartConvert()
        return

    def AddConvertBack(self, data, waifuId, backParam, tick):
        try:
            if data:
                savePath = os.path.dirname(self.curConvertPath)
                if not os.path.isdir(savePath):
                    os.makedirs(savePath)
                f = open(self.curConvertPath, "wb+")
                f.write(data)
                f.close()
                self.tick = tick
                self.resetConvertCnt = 0
                self.curPreConvertId += 1
                self.StartConvert()
            else:
                self.resetConvertCnt += 1
                if self.resetConvertCnt >= 3:
                    self.status = DownloadInfo.Error
                    self.SetConvertStatu(DownloadInfo.Error)
                else:
                    self.StartConvert()
        except Exception as es:
            Log.Error(es)
            self.status = DownloadInfo.Error
            self.SetConvertStatu(DownloadInfo.Error)
        return

    def PauseDownload(self):
        self.status = DownloadInfo.Pause
        self.ClearTask()
        return

    def PauseConvert(self):
        self.ClearConvert()