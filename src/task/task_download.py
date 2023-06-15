import os
from enum import Enum
from functools import partial

from config import config
from config.setting import Setting
from tools.book import BookMgr, BookInfo
from tools.log import Log
from task.qt_task import TaskBase, QtTaskBase
from tools.status import Status
from tools.str import Str


class QtDownloadTask(object):
    Waiting = Str.Waiting
    Reading = Str.Reading
    ReadingPicture = Str.ReadingPicture
    Downloading = Str.Downloading
    Success = Str.Success
    Error = Str.Error
    Cache = Str.Cache

    def __init__(self, downloadId=0):
        self.downloadId = downloadId
        self.downloadCallBack = None       # addData, laveSize
        self.downloadCompleteBack = None   # data, status
        self.statusBack = None
        self.fileSize = 0
        self.url = ""
        self.path = ""
        self.originalName = ""
        self.backParam = None
        self.cleanFlag = ""
        self.lastLaveSize = 0
        self.isInit = False

        self.loadPath = ""    # 只加载
        self.cachePath = ""   # 缓存路径
        self.savePath = ""    # 下载保存路径
        self.isLoadTask = False

        self.bookId = ""      # 下载的bookId
        self.epsId = 0        # 下载的章节
        self.index = 0        # 下载的索引
        self.site = ""
        self.token = ""
        self.resetCnt = 0     # 重试次数
        self.isLocal = True
        self.status = self.Waiting


class TaskDownload(TaskBase, QtTaskBase):

    def __init__(self):
        TaskBase.__init__(self)
        QtTaskBase.__init__(self)
        self.taskObj.downloadBack.connect(self.HandlerTask)
        self.taskObj.downloadStBack.connect(self.HandlerTaskSt)
        self.thread.start()

    def Run(self):
        while True:
            v = self._inQueue.get(True)
            self._inQueue.task_done()
            if v == "":
                break
            self.HandlerDownload({"st": Status.Ok}, (v, QtDownloadTask.Waiting))

    def DownloadBook(self, bookId, index, token, domain, statusBack=None, downloadCallBack=None, completeCallBack=None,
                    backParam=None, loadPath="", cachePath="", savePath="", cleanFlag=None, isInit=False):
        self.taskId += 1
        data = QtDownloadTask(self.taskId)
        data.downloadCallBack = downloadCallBack
        data.downloadCompleteBack = completeCallBack
        data.isInit = isInit
        data.statusBack = statusBack
        data.backParam = backParam
        data.bookId = bookId
        data.token = token
        data.site = domain
        data.index = index
        data.loadPath = loadPath
        data.cachePath = cachePath
        data.savePath = savePath
        self.tasks[self.taskId] = data
        if cleanFlag:
            data.cleanFlag = cleanFlag
            taskIds = self.flagToIds.setdefault(cleanFlag, set())
            taskIds.add(self.taskId)

        Log.Debug("add download info, bookId:{}, token:{}, index:{}, taskId:{}".format(bookId, token, index, self.taskId))
        self._inQueue.put(self.taskId)
        # from server.server import Server
        # from server import req
        # Server().Download(req.DownloadBookReq(url, path, isSaveCache), backParams=self.taskId, cacheAndLoadPath=data.cacheAndLoadPath, loadPath=data.loadPath)
        return self.taskId

    def DownloadCache(self, filePath, completeCallBack=None, backParam = 0, cleanFlag=""):
        self.taskId += 1
        data = QtDownloadTask(self.taskId)
        data.downloadCompleteBack = completeCallBack
        data.loadPath = filePath
        data.backParam = backParam
        data.isLoadTask = True
        if cleanFlag:
            data.cleanFlag = cleanFlag
            taskIds = self.flagToIds.setdefault(cleanFlag, set())
            taskIds.add(self.taskId)
        self.tasks[self.taskId] = data
        self._inQueue.put(self.taskId)
        return self.taskId

    def HandlerDownload(self, data, v):
        (taskId, newStatus) = v
        task = self.tasks.get(taskId)
        if not task:
            return
        backData = {}
        from server import req, ToolUtil
        try:
            assert isinstance(task, QtDownloadTask)
            if task.isLoadTask:
                imgData = ToolUtil.LoadCachePicture(task.loadPath)
                if imgData:
                    TaskBase.taskObj.downloadBack.emit(taskId, len(imgData), b"")
                    TaskBase.taskObj.downloadBack.emit(taskId, 0, imgData)
                else:
                    TaskBase.taskObj.downloadBack.emit(taskId, -Status.FileError, b"")
                return

            isReset = False

            if data["st"] != Status.Ok:
                task.resetCnt += 1

                # 失败了
                if task.resetCnt >= 5:
                    self.SetTaskStatus(taskId, backData, task.Error)
                    return

                isReset = True
            else:
                task.status = newStatus

            info = BookMgr().GetBookBySite(task.bookId, task.site)

            if task.status == task.Waiting:
                isReset or self.SetTaskStatus(taskId, backData, task.Reading)

                if not info or len(info.loadPages) <= 0:
                    self.AddHttpTask(req.BookInfoReq(task.bookId, token=task.token, site=task.site), self.HandlerDownload, (taskId, task.Waiting))
                    return
                task.status = task.Reading

            assert isinstance(info, BookInfo)
            task.token = info.baseInfo.token
            backData["maxPic"] = info.pageInfo.pages
            backData["title"] = info.baseInfo.title
            backData["token"] = info.baseInfo.token

            # if task.isSaveFile:
            #     filePaths = [task.loadPath]
            # else:
            #     # 如果有缓存则不需要以下步骤了
            #     task.cacheAndLoadPath = "{}/{}_{}/{}".format(task.site, task.bookId, task.token, task.index + 1)
            #     filePath2 = os.path.join(os.path.join(Setting.SavePath.value, config.CachePathDir), task.cacheAndLoadPath)
            #     filePaths = [filePath2, task.loadPath]

            # for cachePath in filePaths:
            #     if cachePath:
            #         imgData = ToolUtil.LoadCachePicture(cachePath)
            #         if imgData:
            #             self.SetTaskStatus(taskId, task, backData, status)
            #             TaskBase.taskObj.downloadBack.emit(taskId, len(imgData), imgData)
            #             TaskBase.taskObj.downloadBack.emit(taskId, 0, b"")
            #             return
            if task.status == task.Reading:
                isReset or self.SetTaskStatus(taskId, backData, task.ReadingPicture)
                if not info.pageInfo.showKey:
                    self.AddHttpTask(req.GetBookImgUrl(task.bookId, 1, task.site), self.HandlerDownload)
                    return
                imgUrl = info.pageInfo.picRealUrl.get(task.index + 1)
                # 如果不存在url
                if not imgUrl:
                    # 如果是分页没有加载完
                    #计算当前所在的分页
                    if info.IsNeedLoadPage(task.index):
                        self.AddHttpTask(req.BookInfoReq(task.bookId, page=info.GetPicInPages(task.index), token=task.token, site=task.site), self.HandlerDownload, (taskId, task.Reading))
                        return
                    # 分页加载完，则获取imgUrl
                    else:
                        self.AddHttpTask(req.GetBookImgUrl2(task.bookId, task.index + 1, task.site), self.HandlerDownload, (taskId, task.Reading))
                        return
                task.status = task.ReadingPicture
            if task.status == task.ReadingPicture:
                    status = task.Downloading
                    self.SetTaskStatus(taskId, backData, status)

                    if task.isInit:
                        self.SetTaskStatus(taskId, backData, task.Success)
                        return

                    if task.savePath:
                        if ToolUtil.IsHaveFile(task.savePath):
                            self.SetTaskStatus(taskId, backData, task.Cache)
                            return
                    else:

                        for cachePath in [task.cachePath]:
                            if cachePath:
                                imgData = ToolUtil.LoadCachePicture(cachePath)
                                if imgData:
                                    TaskBase.taskObj.downloadBack.emit(taskId, len(imgData), b"")
                                    TaskBase.taskObj.downloadBack.emit(taskId, 0, imgData)
                                    return

                    self.AddDownloadTask(
                        imgUrl, "", task.downloadCallBack, task.downloadCompleteBack, task.statusBack,
                        task.backParam, task.loadPath, task.cachePath, task.savePath, task.cleanFlag)
        except Exception as es:
            Log.Error(es)
        return

    def SetTaskStatus(self, taskId, backData, status):
        backData["st"] = status
        self.taskObj.downloadStBack.emit(taskId, dict(backData))
        return

    def CallBookBack(self, data, task):
        try:
            if not task.statusBack:
                return
            if task.backParam is not None:
                task.statusBack(data, task.backParam)
            else:
                task.statusBack(data)
        except Exception as es:
            Log.Error(es)

    def DownloadTask(self, url, path, downloadCallBack=None, completeCallBack=None, downloadStCallBack=None, backParam=None, loadPath="", cachePath="", savePath="", cleanFlag="", isReload=False):
        self.taskId += 1
        data = QtDownloadTask(self.taskId)
        data.downloadCallBack = downloadCallBack
        data.downloadCompleteBack = completeCallBack
        data.backParam = backParam
        data.statusBack = downloadStCallBack
        data.isReload = isReload
        data.url = url
        data.path = path
        data.loadPath = loadPath
        data.cachePath = cachePath
        data.savePath = savePath
        self.tasks[self.taskId] = data
        if cleanFlag:
            data.cleanFlag = cleanFlag
            taskIds = self.flagToIds.setdefault(cleanFlag, set())
            taskIds.add(self.taskId)

        from server.server import Server
        from server import req
        Log.Debug("add download info, taskId:{}, url:{}".format(self.taskId, url))
        Server().Download(req.DownloadBookReq(url, data.loadPath, data.cachePath, data.savePath, data.isReload),
                          backParams=self.taskId)
        return self.taskId

    def HandlerTask(self, downloadId, laveFileSize, data, isCallBack=True):
        Log.Debug("download back, taskId:{}, laveSize:{}".format(downloadId, laveFileSize))
        info = self.tasks.get(downloadId)
        if not info:
            return
        assert isinstance(info, QtDownloadTask)

        # 表示保存失败了
        if laveFileSize == -2:
            v = {"st": Status.SaveError}
            self.CallBookBack(v, info)
            return
        st = Str.Error
        if laveFileSize < -2:
            st = - laveFileSize

        if laveFileSize < 0 and data == b"":
            try:
                if info.downloadCompleteBack:
                    if info.backParam is not None:
                        info.downloadCompleteBack(b"", st, info.backParam)
                    else:
                        info.downloadCompleteBack(b"", st)
            except Exception as es:
                Log.Error(es)
            self.ClearDownloadTask(downloadId)
            return

        if info.lastLaveSize <= 0:
            info.lastLaveSize = laveFileSize

        if info.downloadCallBack:
            try:
                if info.backParam is not None:
                    info.downloadCallBack(info.lastLaveSize-laveFileSize, laveFileSize, info.backParam)
                else:
                    info.downloadCallBack(info.lastLaveSize-laveFileSize, laveFileSize)
            except Exception as es:
                Log.Error(es)
            info.lastLaveSize = laveFileSize

        if laveFileSize == 0 and data != b"":
            if info.downloadCompleteBack:
                try:
                    if info.cleanFlag:
                        taskIds = self.flagToIds.get(info.cleanFlag, set())
                        taskIds.discard(info.downloadId)
                    if info.backParam is not None:
                        info.downloadCompleteBack(data, Status.Ok, info.backParam)
                    else:
                        info.downloadCompleteBack(data, Status.Ok)
                except Exception as es:
                    Log.Error(es)
            self.ClearDownloadTask(downloadId)

    def HandlerTaskSt(self, downloadId, data):
        task = self.tasks.get(downloadId)
        if not task:
            return
        assert isinstance(task, QtDownloadTask)
        try:
            self.CallBookBack(data, task)
            status = task.status
            if status == task.Downloading or status == task.Error or status == task.Cache:
                self.ClearDownloadTask(downloadId)
        except Exception as es:
            Log.Error(es)

    def ClearDownloadTask(self, downloadId):
        info = self.tasks.get(downloadId)
        if not info:
            return
        del self.tasks[downloadId]
