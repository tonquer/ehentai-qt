import json
import os
import pickle
import re

import requests

from conf import config
from src.qt.util.qttask import QtTask
from src.server import req, Status, Log, ToolUtil
from .server import handler, Task, Server


@handler(req.CheckUpdateReq)
class CheckUpdateHandler(object):
    def __call__(self, backData):
        if not backData.GetText() or backData.status == Status.NetError:
            if backData.backParam:
                data = b""
                QtTask().taskBack.emit(backData.backParam, pickle.dumps(data))
            return

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
                QtTask().taskBack.emit(backData.backParam, pickle.dumps(data))


@handler(req.GetUserIdReq)
class GetUserIdReqHandler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            userId, userName = ToolUtil.ParseLoginUserName(task.res.raw.text)
            if userId:
                data["st"] = Status.Ok
                data["userId"] = userId
                data["userName"] = userName
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                QtTask().taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.LoginReq)
class LoginReqHandler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            parseSt = ToolUtil.ParseLoginUserName(task.res.raw.text)
            from requests import Response
            assert isinstance(task.res.raw, Response)
            cookies = requests.utils.dict_from_cookiejar(task.res.raw.cookies)
            memberId = cookies.get("ipb_member_id")
            ipbHash = cookies.get("ipb_pass_hash")
            sessionId = cookies.get("ipb_session_id")
            coppa = cookies.get("ipb_coppa")
            if memberId and ipbHash:
                data["ipb_member_id"] = memberId
                data["ipb_pass_hash"] = ipbHash
                data["ipb_session_id"] = sessionId
                data["ipb_coppa"] = coppa
                Log.Info("login success, {}".format(cookies))
                st = Status.Ok
                data["st"] = st
            else:
                data["st"] = ToolUtil.ParseLoginResult(task.res.raw.text)
                Log.Info("login error, {}".format(cookies))
            # cookies = task.res.raw.headers.get("Set-Cookie", "")
            # print(cookies)
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                QtTask().taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.HomeReq)
class HomeReqHandler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            curNum, maxNum = ToolUtil.ParseHomeInfo(task.res.raw.text)
            data["st"] = Status.Ok
            data["curNum"] = curNum
            data["maxNum"] = maxNum
            pass
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                QtTask().taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetIndexInfoReq)
@handler(req.GetCategoryInfoReq)
class GetIndexInfoReqHandler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            if not task.res.raw.text:
                data["st"] = Status.Error
            else:
                if task.req.site == "exhentai":
                    cookies = requests.utils.dict_from_cookiejar(task.res.raw.cookies)
                    igneous = cookies.get("igneous")
                    if igneous:
                        data["igneous"] = igneous
                    else:
                        for raw in task.res.raw.history:
                            cookies = requests.utils.dict_from_cookiejar(raw.cookies)
                            igneous = cookies.get("igneous")
                            if igneous:
                                data["igneous"] = igneous
                                break
                bookList, maxPages = ToolUtil.ParseBookIndex(task.res.raw.text)
                from src.book.book import BookMgr
                BookMgr().UpdateBookInfoList(bookList, task.req.site)
                data["st"] = Status.Ok
                data["bookList"] = bookList
                data["maxPages"] = maxPages
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                QtTask().taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetFavoritesReq)
class GetFavoritesReqHandler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            bookList, maxPages = ToolUtil.ParseBookIndex(task.res.raw.text)
            favoriteList = ToolUtil.ParseFavorite(task.res.raw.text)
            from src.book.book import BookMgr
            BookMgr().UpdateBookInfoList(bookList, task.req.site)
            data["st"] = Status.Ok
            data["bookList"] = bookList
            data["maxPages"] = maxPages
            data["favoriteList"] = favoriteList
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                QtTask().taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.BookInfoReq)
class BookInfoReqHandler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            info, maxPage = ToolUtil.ParseBookInfo(task.res.raw.text)
            from src.book.book import BookMgr
            BookMgr().UpdateBookInfo(task.req.bookId, info, task.req.page, maxPage, task.req.site)

            if task.req.page == 1:
                # TODO 预加载第一页
                Server().Send(req.GetBookImgUrl(task.req.bookId, 1, task.req.site), isASync=False)

                # TODO 加载剩余分页
                # for i in range(1+1, maxPage+1):
                #     Server().Send(req.BookInfoReq(task.req.bookId, i), isASync=False)
            data["maxPages"] = maxPage
            data["st"] = Status.Ok
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                QtTask().taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetBookImgUrl)
class GetBookImgUrlReqHandler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            imgUrl, imgKey = ToolUtil.ParsePictureInfo(task.res.raw.text)
            from src.book.book import BookMgr
            BookMgr().UpdateImgKey(task.req.bookId, imgKey, task.req.site)
            BookMgr().UpdateImgUrl(task.req.bookId, task.req.index, imgUrl, task.req.site)
            data["st"] = Status.Ok
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                QtTask().taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetBookImgUrl2)
class GetBookImgUrl2ReqHandler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            imgUrl = ToolUtil.ParsePictureInfo2(task.res.raw.text)
            from src.book.book import BookMgr
            BookMgr().UpdateImgUrl(task.req.bookId, task.req.index, imgUrl, task.req.site)
            data["st"] = Status.Ok
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                QtTask().taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.AddFavoritesReq)
class AddFavoritesReqHandler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            note, favorites, isUpdate = ToolUtil.ParseAddFavorite(task.res.raw.text)
            data["st"] = Status.Ok
            data["note"] = note
            data["favorites"] = favorites
            data["update"] = isUpdate
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                QtTask().taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.AddFavorites2Req)
class AddFavorites2ReqHandler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            return
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                QtTask().taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.DelFavoritesReq)
class DelFavoritesReqHandler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            return
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                QtTask().taskBack.emit(task.backParam, pickle.dumps(data))


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
                        QtTask().downloadBack.emit(backData.backParam, -r.status_code, b"")
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


@handler(req.SpeedTestPingReq)
class SpeedTestPingHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": str(0)}
        try:
            if task.status != Status.Ok:
                return
            if hasattr(task.res.raw, "elapsed"):
                data["data"] = str(task.res.raw.elapsed.total_seconds())
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                QtTask().taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.DnsOverHttpsReq)
class DnsOverHttpsReqHandler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            info = json.loads(task.res.raw.text)
            data['Answer'] = info.get("Answer")
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                QtTask().taskBack.emit(task.backParam, pickle.dumps(data))