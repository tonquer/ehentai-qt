import json
import os
import re

import requests

from conf import config
from src.qt.util.qttask import QtTask
from .server import handler, Task, Server
from src.server import req, Status, Log, ToolUtil


@handler(req.CheckUpdateReq)
class CheckUpdateHandler(object):
    def __call__(self, backData):
        updateInfo = re.findall(r"<meta property=\"og:description\" content=\"([^\"]*)\"", backData.res.raw.text)
        if updateInfo:
            data = updateInfo[0]
        else:
            data = ""

        info = re.findall(r"\d+\d*", os.path.basename(backData.res.raw.url))
        version = int(info[0]) * 100 + int(info[1]) * 10 + int(info[2]) * 1
        info2 = re.findall(r"\d+\d*", os.path.basename(config.UpdateVersion))
        curversion = int(info2[0]) * 100 + int(info2[1]) * 10 + int(info2[2]) * 1

        data = "\n\nv" + ".".join(info) + "\n" + data
        if version > curversion:
            if backData.backParam:
                QtTask().taskBack.emit(backData.backParam, data)


@handler(req.LoginReq)
class LoginReqHandler(object):
    def __call__(self, task: Task):
        st = Status.NetError
        try:
            from requests import Response
            assert isinstance(task.res.raw, Response)
            cookies = requests.utils.dict_from_cookiejar(task.res.raw.cookies)
            memberId = cookies.get("ipb_member_id")
            ipbHash = cookies.get("ipb_pass_hash")
            if memberId and ipbHash:
                Log.Info("login success, {}".format(cookies))
                st = Status.Ok
            else:
                Log.Info("login error, {}".format(cookies))
                st = Status.UserError
            # cookies = task.res.raw.headers.get("Set-Cookie", "")
            # print(cookies)
            pass
        except Exception as es:
            Log.Error(es)
        if task.backParam:
            QtTask().taskBack.emit(task.backParam, st)


@handler(req.HomeReq)
class HomeReqHandler(object):
    def __call__(self, task: Task):
        try:
            pass
        except Exception as es:
            Log.Error(es)
        if task.backParam:
            QtTask().taskBack.emit(task.backParam, "")


@handler(req.GetIndexInfoReq)
class GetIndexInfoReqHandler(object):
    def __call__(self, task: Task):
        bookList = []
        maxPages = 1
        st = Status.NetError
        try:
            bookList, maxPages = ToolUtil.ParseBookIndex(task.res.raw.text)
            from src.book.book import BookMgr
            BookMgr().UpdateBookInfoList(bookList)
            st = Status.Ok
        except Exception as es:
            Log.Error(es)
        if task.backParam:
            QtTask().taskBack.emit(task.backParam, json.dumps({"st": st, "bookList": [i.baseInfo.id for i in bookList], "pages": maxPages}))


@handler(req.BookInfoReq)
class BookInfoReqHandler(object):
    def __call__(self, task):
        st = Status.Error
        try:
            info, maxPage = ToolUtil.ParseBookInfo(task.res.raw.text)
            from src.book.book import BookMgr
            st = BookMgr().UpdateBookInfo(task.req.bookId, info)

            if task.req.page == 1:
                # TODO 预加载第一页
                Server().Send(req.GetBookImgUrl(task.req.bookId, 1), isASync=False)

                # TODO 加载剩余分页
                for i in range(1+1, maxPage+1):
                    Server().Send(req.BookInfoReq(task.req.bookId, i), isASync=False)
        except Exception as es:
            Log.Error(es)
        if task.backParam:
            QtTask().taskBack.emit(task.backParam, st)


@handler(req.GetBookImgUrl)
class GetBookImgUrlReqHandler(object):
    def __call__(self, task):
        try:
            imgUrl, imgKey = ToolUtil.ParsePictureInfo(task.res.raw.text)
            from src.book.book import BookMgr
            BookMgr().UpdateImgKey(task.req.bookId, imgKey)
            BookMgr().UpdateImgUrl(task.req.bookId, task.req.index, imgUrl)
        except Exception as es:
            Log.Error(es)
        if task.backParam:
            QtTask().taskBack.emit(task.backParam, "")


@handler(req.GetBookImgUrl2)
class GetBookImgUrl2ReqHandler(object):
    def __call__(self, task):
        try:
            imgUrl = ToolUtil.ParsePictureInfo2(task.res.raw.text)
            from src.book.book import BookMgr
            BookMgr().UpdateImgUrl(task.req.bookId, task.req.index, imgUrl)
        except Exception as es:
            Log.Error(es)
        if task.backParam:
            QtTask().taskBack.emit(task.backParam, "")


@handler(req.DownloadBookReq)
class DownloadBookReq(object):
    def __call__(self, backData):
        if backData.status != Status.Ok:
            if backData.backParam:
                QtTask().downloadBack.emit(backData.backParam, -1, b"")
        else:
            r = backData.res
            try:
                if r.status_code != 200:
                    if backData.backParam:
                        QtTask().downloadBack.emit(backData.backParam, -1, b"")
                    return
                fileSize = int(r.headers.get('Content-Length', 0))
                getSize = 0
                data = b""
                for chunk in r.iter_content(chunk_size=1024):
                    if backData.backParam:
                        QtTask().downloadBack.emit(backData.backParam, fileSize-getSize, chunk)
                    getSize += len(chunk)
                    data += chunk
                if backData.backParam:
                    QtTask().downloadBack.emit(backData.backParam, 0, b"")
                # Log.Info("size:{}, url:{}".format(ToolUtil.GetDownloadSize(fileSize), backData.req.url))
                if backData.cacheAndLoadPath and config.IsUseCache and len(data) > 0:
                    filePath = backData.cacheAndLoadPath
                    fileDir = os.path.dirname(filePath)
                    if not os.path.isdir(fileDir):
                        os.makedirs(fileDir)

                    with open(filePath, "wb+") as f:
                        f.write(data)
                    Log.Debug("add download cache, cachePath:{}".format(filePath))
            except Exception as es:
                Log.Error(es)
                if backData.backParam:
                    QtTask().downloadBack.emit(backData.backParam, -1, b"")
