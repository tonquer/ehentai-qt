import pickle
import threading
from queue import Queue

import requests
import urllib3

import server.res as res
from config import config
from config.setting import Setting
from qt_owner import QtOwner
from tools.tool import ToolUtil
from tools.singleton import Singleton
from tools.log import Log
from tools.status import Status

urllib3.disable_warnings()

# _orig_create_connection = connection.create_connection
# https://ehwiki.org/wiki/IPs
host_table = {}


# def _dns_resolver(host):
#     if host in host_table:
#         return host_table[host]
#     else:
#         return host
#
#
# def patched_create_connection(address, *args, **kwargs):
#     host, port = address
#     hostname = _dns_resolver(host)
#     return _orig_create_connection((hostname, port), *args, **kwargs)


# connection.create_connection = patched_create_connection


# urllib3.contrib.pyopenssl.HAS_SNI = False
# urllib3.contrib.pyopenssl.inject_into_urllib3()


def handler(request):
    def generator(handler):
        Server().handler[request] = handler()
        return handler
    return generator


class Task(object):
    def __init__(self, request, backParam=""):
        self.req = request
        self.res = None
        self.backParam = backParam
        self.status = Status.Ok

    @property
    def host(self):
        if "host" in self.req.headers:
            return self.req.headers["host"]
        return ""

    @property
    def bakParam(self):
        return self.backParam

    @bakParam.setter
    def bakParam(self, v):
        self.backParam = v

    @property
    def timeout(self):
        return self.req.timeout

    def GetText(self):
        if not self.res:
            return ""
        if hasattr(self.res, "raw"):
            getattr(self.res.raw, "text", "")
        return ""


class Server(Singleton, threading.Thread):
    def __init__(self) -> None:
        super().__init__()
        threading.Thread.__init__(self)
        self.isLogin = False
        self.handler = {}
        self.session = requests.session()
        self.address = ""
        self.imageServer = ""
        self.dns_host = {}

        self._inQueue = Queue()
        self._downloadQueue = Queue()
        self.threadHandler = 0
        self.threadNum = config.ThreadNum
        self.downloadNum = config.DownloadThreadNum

        for i in range(self.threadNum):
            thread = threading.Thread(target=self.Run)
            thread.setDaemon(True)
            thread.start()

        for i in range(Setting.DownloadNum.value):
            thread = threading.Thread(target=self.RunDownload)
            thread.setDaemon(True)
            thread.start()

    def Run(self):
        while True:
            task = self._inQueue.get(True)
            self._inQueue.task_done()
            try:
                if task == "":
                    break
                self._Send(task)
            except Exception as es:
                Log.Error(es)
        pass

    def Stop(self):
        for i in range(self.threadNum):
            self._inQueue.put("")
        for i in range(self.downloadNum):
            self._downloadQueue.put("")

    def RunDownload(self):
        while True:
            task = self._downloadQueue.get(True)
            self._downloadQueue.task_done()
            try:
                if task == "":
                    break
                self._Download(task)
            except Exception as es:
                Log.Error(es)
        pass

    def UpdateDns(self, domain, address):
        host_table[domain] = address

    def UpdateSni(self):
        pass
        # if Setting.IsCloseSNI.value:
        #     urllib3.contrib.pyopenssl.HAS_SNI = False
        #     urllib3.contrib.pyopenssl.inject_into_urllib3()
        # else:
        #     urllib3.contrib.pyopenssl.HAS_SNI = True
        #     urllib3.contrib.pyopenssl.inject_into_urllib3()

    def ClearDns(self):
        host_table.clear()

    def __DealHeaders(self, request, token):
        host = ToolUtil.GetUrlHost(request.url)
        mapHost = config.DomainMapping.get(host, host)

        if Setting.IpDirect.value:
            if mapHost in host_table:
                ip = host_table[mapHost]
                request.headers["host"] = host
                request.url = request.url.replace(host, ip)

        if not request.isUseHttps:
            request.url = request.url.replace("https://", "http://")

    def Send(self, request, token="", backParam="", isASync=True):
            self.__DealHeaders(request, token)
            if isASync:
                self._inQueue.put(Task(request, backParam))
            else:
                self._Send(Task(request, backParam))

    def _Send(self, task):
        try:
            Log.Info("request-> backId:{}, {}".format(task.backParam, task.req))
            if QtOwner().isOfflineModel:
                task.status = Status.OfflineModel
                data = {"st": Status.OfflineModel, "data": ""}
                from task.qt_task import TaskBase
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))
                return

            if task.req.method.lower() == "post":
                self.Post(task)
            elif task.req.method.lower() == "get":
                self.Get(task)
            else:
                return
        except Exception as es:
            if isinstance(es, requests.exceptions.ConnectTimeout):
                task.status = Status.ConnectErr
            elif isinstance(es, requests.exceptions.ReadTimeout):
                task.status = Status.TimeOut
            elif isinstance(es, requests.exceptions.SSLError):
                if "WSAECONNRESET" in es.__repr__():
                    task.status = Status.ResetErr
                else:
                    task.status = Status.SSLErr
            elif isinstance(es, requests.exceptions.ProxyError):
                task.status = Status.ProxyError
            elif isinstance(es, ConnectionResetError):
                task.status = Status.ResetErr
            elif "ConnectionResetError" in es.__repr__():
                task.status = Status.ResetErr
            else:
                task.status = Status.NetError
            Log.Warn(task.req.url + " " + es.__repr__())
            Log.Debug(es)
        finally:
            Log.Info("response-> backId:{}, {}, {}".format(task.backParam, task.req.__class__.__name__, task.res))
        try:
            self.handler.get(task.req.__class__)(task)
            if task.res.raw:
                task.res.raw.close()
        except Exception as es:
            Log.Warn("task: {}, error".format(task.req.__class__))
            Log.Error(es)

    def Post(self, task):
        request = task.req
        if request.params == None:
            request.params = {}

        if request.headers == None:
            request.headers = {}

        if self.isLogin:
            cookie = {"igneous": Setting.Igneous.value, "ipb_member_id": Setting.IpbMemberId.value, "ipb_pass_hash": Setting.IpbPassHash.value}
        else:
            cookie = {}
        task.res = res.BaseRes("", False)

        history = []
        for i in range(10):
            r = self.session.post(request.url, proxies=request.proxy, headers=request.headers, data=request.params, timeout=task.timeout, verify=False, cookies=cookie, allow_redirects=False)
            if r.status_code == 302 or r.status_code == 301:
                next = r.headers.get('Location')
                request.url = next
                history.append(r)
                self.__DealHeaders(request, "")
            else:
                break
        r.history = history
        task.res = res.BaseRes(r, request.isParseRes)
        return task

    def Get(self, task):
        request = task.req
        if request.params == None:
            request.params = {}

        if request.headers == None:
            request.headers = {}

        if self.isLogin:
            cookie = {"igneous": Setting.Igneous.value, "ipb_member_id": Setting.IpbMemberId.value, "ipb_pass_hash": Setting.IpbPassHash.value}
        else:
            cookie = {}
        task.res = res.BaseRes("", False)
        history = []
        for i in range(10):
            r = self.session.get(request.url, proxies=request.proxy, headers=request.headers, timeout=task.timeout, verify=False, cookies=cookie, allow_redirects=False)
            if r.status_code == 302 or r.status_code == 301:
                next = r.headers.get('Location')
                request.url = next
                history.append(r)
                self.__DealHeaders(request, "")
            else:
                break
        r.history = history
        task.res = res.BaseRes(r, request.isParseRes)
        return task

    def Download(self, request, token="", backParams="", isASync=True):
        self.__DealHeaders(request, token)
        task = Task(request, backParams)
        if isASync:
            self._downloadQueue.put(task)
        else:
            self._Download(task)

    def _Download(self, task):
        try:
            if not task.req.isReload:
                for cachePath in [task.req.loadPath, task.req.cachePath]:
                    if cachePath and task.backParam:
                        data = ToolUtil.LoadCachePicture(cachePath)
                        if data:
                            from task.qt_task import TaskBase
                            TaskBase.taskObj.downloadBack.emit(task.backParam, len(data), b"")
                            TaskBase.taskObj.downloadBack.emit(task.backParam, 0, data)
                            Log.Info("request cache -> backId:{}, {}".format(task.backParam, task.req))
                            return
            request = task.req
            if request.params == None:
                request.params = {}

            if request.headers == None:
                request.headers = {}

            Log.Info("request-> backId:{}, {}".format(task.backParam, task.req))
            cookie = {"igneous": Setting.Igneous.value, "ipb_member_id": Setting.IpbMemberId.value,
                      "ipb_pass_hash": Setting.IpbPassHash.value}
            r = self.session.get(request.url, proxies=request.proxy, headers=request.headers, stream=True, timeout=task.timeout, verify=False, cookies=cookie)
            # task.res = res.BaseRes(r)
            task.res = r
        # except ConnectTimeoutError as es:
        #     Log.Warn(task.req.url + " " + es.__repr__())
        #     task.status = Status.Timeout
        except Exception as es:
            if isinstance(es, requests.exceptions.ConnectTimeout):
                task.status = Status.ConnectErr
            elif isinstance(es, requests.exceptions.ReadTimeout):
                task.status = Status.TimeOut
            elif isinstance(es, requests.exceptions.SSLError):
                if "WSAECONNRESET" in es.__repr__():
                    task.status = Status.ResetErr
                else:
                    task.status = Status.SSLErr
            elif isinstance(es, requests.exceptions.ProxyError):
                task.status = Status.ProxyError
            elif isinstance(es, ConnectionResetError):
                task.status = Status.ResetErr
            else:
                task.status = Status.NetError
            Log.Warn(task.req.url + " " + es.__repr__())
        self.handler.get(task.req.__class__)(task)
        if task.res:
            task.res.close()

    def TestSpeedPing(self, request, backParams=""):
        self.__DealHeaders(request, "")
        task = Task(request, backParams)
        self._inQueue.put(task)
