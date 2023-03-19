import json
import os
import pickle
import re
import time

import requests

from config import config
from task.qt_task import TaskBase
from server import req
from tools.status import Status
from tools.log import Log
from tools.tool import ToolUtil
from .server import handler, Task, Server


@handler(req.CheckUpdateReq)
class CheckUpdateHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": ""}
        try:
            if not task.res.GetText() or task.status == Status.NetError:
                return
            if task.res.raw.status_code != 200:
                return

            updateInfo = re.findall(r"<meta property=\"og:description\" content=\"([^\"]*)\"", task.res.raw.text)
            if updateInfo:
                rawData = updateInfo[0]
            else:
                rawData = ""

            versionInfo = re.findall("<meta property=\"og:url\" content=\".*tag/([^\"]*)\"", task.res.raw.text)
            if versionInfo:
                verData = versionInfo[0]
            else:
                verData = ""

            info = verData.replace("v", "").split(".")
            version = int(info[0]) * 100 + int(info[1]) * 10 + int(info[2]) * 1
            info2 = re.findall(r"\d+\d*", os.path.basename(config.UpdateVersion))
            curversion = int(info2[0]) * 100 + int(info2[1]) * 10 + int(info2[2]) * 1

            rawData = "\n\nv" + ".".join(info) + "\n" + rawData

            if version > curversion:
                data["data"] = rawData
            else:
                data["data"] = "no"
        except Exception as es:
            pass
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.CheckPreUpdateReq)
class CheckPreUpdateReqHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": ""}
        try:
            if not task.res.GetText() or task.status == Status.NetError:
                return
            if task.res.raw.status_code != 200:
                return
            rawData = json.loads(task.res.raw.text)
            if not rawData:
                return
            v = rawData[0]
            verData = v.get("tag_name")
            info = verData.replace("v", "").split(".")
            version = int(info[0]) * 100 + int(info[1]) * 10 + int(info[2]) * 1
            info2 = re.findall(r"\d+\d*", os.path.basename(config.UpdateVersion))
            curversion = int(info2[0]) * 100 + int(info2[1]) * 10 + int(info2[2]) * 1

            rawData = v.get("body")

            if version > curversion:
                data["data"] = rawData
            else:
                data["data"] = "no"

        except Exception as es:
            pass
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


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
            Log.ParseError(es, task.req.url, task.res.GetText())
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


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
            Log.ParseError(es, task.req.url, task.res.GetText())
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


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
            Log.ParseError(es, task.req.url, task.res.GetText())
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetIndexInfoReq)
@handler(req.GetRankInfoReq)
@handler(req.GetCategoryInfoReq)
class GetIndexInfoReqHandler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
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
                if not task.res.raw.text:
                    data["st"] = Status.Error
                    return
                bookList, nextId = ToolUtil.ParseBookIndex(task.res.raw.text)
                from tools.book import BookMgr
                BookMgr().UpdateBookInfoList(bookList, task.req.site)
                data["st"] = Status.Ok
                data["bookList"] = bookList
                data["nextId"] = nextId
        except Exception as es:
            data["st"] = Status.ParseError
            Log.ParseError(es, task.req.url, task.res.GetText())
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetFavoritesReq)
class GetFavoritesReqHandler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            bookList, nextId = ToolUtil.ParseBookIndex(task.res.raw.text)
            favoriteList = ToolUtil.ParseFavorite(task.res.raw.text)
            from tools.book import BookMgr
            BookMgr().UpdateBookInfoList(bookList, task.req.site)
            data["st"] = Status.Ok
            data["bookList"] = bookList
            data["nextId"] = nextId
            data["favoriteList"] = favoriteList
        except Exception as es:
            data["st"] = Status.ParseError
            Log.ParseError(es, task.req.url, task.res.GetText())
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.BookInfoReq)
class BookInfoReqHandler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            st, msg, info, maxPage, _ = ToolUtil.ParseBookInfo(task.res.raw.text)
            if st == Status.Ok:
                from tools.book import BookMgr
                BookMgr().UpdateBookInfo(task.req.bookId, info, task.req.page, maxPage, task.req.site)

                if task.req.page == 1:
                    # TODO 预加载第一页
                    Server().Send(req.GetBookImgUrl(task.req.bookId, 1, task.req.site), isASync=False)

                    # TODO 加载剩余分页
                    # for i in range(1+1, maxPage+1):
                    #     Server().Send(req.BookInfoReq(task.req.bookId, i), isASync=False)
            data["maxPages"] = maxPage
            data["msg"] = msg
            data["st"] = st
        except Exception as es:
            data["st"] = Status.ParseError
            Log.ParseError(es, task.req.url, task.res.GetText())
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.SendCommentReq)
class SendCommentReqHandler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            st, errMsg, info, maxPage, commentError = ToolUtil.ParseBookInfo(task.res.raw.text)
            if not commentError:
                from tools.book import BookMgr
                BookMgr().UpdateBookInfo(task.req.bookId, info, task.req.page, maxPage, task.req.site)
                data["st"] = Status.Ok
                data["msg"] = commentError
            else:
                data["st"] = Status.Ok
                data["msg"] = commentError
        except Exception as es:
            data["st"] = Status.ParseError
            Log.ParseError(es, task.req.url, task.res.GetText())
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetBookImgUrl)
class GetBookImgUrlReqHandler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            imgUrl, imgKey = ToolUtil.ParsePictureInfo(task.res.raw.text)
            from tools.book import BookMgr
            BookMgr().UpdateImgKey(task.req.bookId, imgKey, task.req.site)
            BookMgr().UpdateImgUrl(task.req.bookId, task.req.index, imgUrl, task.req.site)
            data["st"] = Status.Ok
        except Exception as es:
            data["st"] = Status.ParseError
            Log.ParseError(es, task.req.url, task.res.GetText())
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetBookImgUrl2)
class GetBookImgUrl2ReqHandler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            imgUrl = ToolUtil.ParsePictureInfo2(task.res.raw.text)
            from tools.book import BookMgr
            BookMgr().UpdateImgUrl(task.req.bookId, task.req.index, imgUrl, task.req.site)
            data["st"] = Status.Ok
        except Exception as es:
            data["st"] = Status.ParseError
            Log.ParseError(es, task.req.url, task.res.GetText())
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


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
            Log.ParseError(es, task.req.url, task.res.GetText())
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.AddFavorites2Req)
class AddFavorites2ReqHandler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            return
        except Exception as es:
            data["st"] = Status.ParseError
            Log.ParseError(es, task.req.url, task.res.GetText())
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.DelFavoritesReq)
class DelFavoritesReqHandler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            return
        except Exception as es:
            data["st"] = Status.ParseError
            Log.ParseError(es, task.req.url, task.res.GetText())
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.DownloadBookReq)
class DownloadBookReq(object):
    def __call__(self, backData):
        if backData.status != Status.Ok:
            if backData.backParam:
                TaskBase.taskObj.downloadBack.emit(backData.backParam, -1, b"")
        else:
            r = backData.res
            try:
                if r.status_code != 200:
                    if backData.backParam:
                        TaskBase.taskObj.downloadBack.emit(backData.backParam, -r.status_code, b"")
                    return
                fileSize = int(r.headers.get('Content-Length', 0))
                getSize = 0
                data = b""

                now = time.time()

                # 网速快，太卡了，优化成最多100ms一次
                for chunk in r.iter_content(chunk_size=4096):
                    cur = time.time()
                    tick = cur - now
                    if tick >= 0.1:
                        if backData.backParam and fileSize - getSize > 0:
                            TaskBase.taskObj.downloadBack.emit(backData.backParam, fileSize - getSize, b"")
                        now = cur

                    getSize += len(chunk)
                    data += chunk

                # Log.Info("size:{}, url:{}".format(ToolUtil.GetDownloadSize(fileSize), backData.req.url))
                _, _, mat, _ = ToolUtil.GetPictureSize(data)
                if config.IsUseCache and len(data) > 0:
                    try:
                        for path in [backData.req.cachePath, backData.req.savePath]:
                            filePath = path
                            if not path:
                                continue
                            fileDir = os.path.dirname(filePath)
                            if not os.path.isdir(fileDir):
                                os.makedirs(fileDir)

                            with open(filePath+"."+mat, "wb+") as f:
                                f.write(data)
                            Log.Debug("add download cache, cachePath:{}".format(filePath))
                    except Exception as es:
                        Log.Error(es)
                        # 保存失败了
                        if backData.backParam:
                            TaskBase.taskObj.downloadBack.emit(backData.backParam, -2, b"")

                if backData.backParam:
                    TaskBase.taskObj.downloadBack.emit(backData.backParam, 0, data)

            except Exception as es:
                backData.status = Status.DownloadFail
                Log.Error(es)
                if backData.backParam:
                    TaskBase.taskObj.downloadBack.emit(backData.backParam, -backData.status, b"")


@handler(req.SpeedTestPingReq)
class SpeedTestPingHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        if hasattr(task.res.raw, "elapsed"):
            if task.res.raw.status_code == 401 or task.res.raw.status_code == 200:
                data["data"] = str(task.res.raw.elapsed.total_seconds()*1000)
            else:
                data["st"] = Status.Error
                data["data"] = str(task.res.raw.elapsed.total_seconds()*1000)
            TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))
        else:
            data["data"] = "0"
            TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


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
            Log.ParseError(es, task.req.url, task.res.GetText())
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))