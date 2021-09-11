import threading
from queue import Queue

import threading
from queue import Queue

import requests
import urllib3

import src.server.res as res
from conf import config
from src.util import ToolUtil, Singleton, Log
from src.util.status import Status

urllib3.disable_warnings()


import urllib3
import urllib3.contrib.pyopenssl

from urllib3.util import connection


_orig_create_connection = connection.create_connection
# https://ehwiki.org/wiki/IPs
host_table = {}


def _dns_resolver(host):
    if host in host_table:
        return host_table[host]
    else:
        return host


def patched_create_connection(address, *args, **kwargs):
    host, port = address
    hostname = _dns_resolver(host)
    return _orig_create_connection((hostname, port), *args, **kwargs)


connection.create_connection = patched_create_connection


urllib3.contrib.pyopenssl.HAS_SNI = False
urllib3.contrib.pyopenssl.inject_into_urllib3()


def handler(request):
    def generator(handler):
        Server().handler[request] = handler()
        return handler
    return generator


class Task(object):
    def __init__(self, request, backParam="", cacheAndLoadPath="", loadPath=""):
        self.req = request
        self.res = None
        self.backParam = backParam
        self.status = Status.Ok
        self.cacheAndLoadPath = cacheAndLoadPath
        self.loadPath = loadPath

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

        for i in range(self.downloadNum):
            thread = threading.Thread(target=self.RunDownload)
            thread.setDaemon(True)
            thread.start()

    def Run(self):
        while True:
            try:
                task = self._inQueue.get(True)
            except Exception as es:
                continue
                pass
            self._inQueue.task_done()
            try:
                self._Send(task)
            except Exception as es:
                Log.Error(es)
        pass

    def RunDownload(self):
        while True:
            task = self._downloadQueue.get(True)
            self._downloadQueue.task_done()
            try:
                self._Download(task)
            except Exception as es:
                Log.Error(es)
        pass

    def UpdateDns(self, domain, address):
        host_table[domain] = address

    def ClearDns(self):
        host_table.clear()

    def __DealHeaders(self, request, token):
        host = ToolUtil.GetUrlHost(request.url)

    def Send(self, request, token="", backParam="", isASync=True):
        self.__DealHeaders(request, token)
        if isASync:
            self._inQueue.put(Task(request, backParam))
        else:
            self._Send(Task(request, backParam))

    def _Send(self, task):
        try:
            Log.Info("request-> backId:{}, {}".format(task.backParam, task.req))
            if task.req.method.lower() == "post":
                self.Post(task)
            elif task.req.method.lower() == "get":
                self.Get(task)
            else:
                return
        except Exception as es:
            task.status = Status.NetError
            Log.Warn(task.req.url + " " + es.__repr__())
            Log.Debug(es)
        finally:
            Log.Info("response-> backId:{}, {}, {}".format(task.backParam, task.req.__class__.__name__, task.res))
        try:
            self.handler.get(task.req.__class__)(task)
            if hasattr(task.res, "raw"):
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

        r = self.session.post(request.url, proxies=request.proxy, headers=request.headers, data=request.params, timeout=task.timeout, verify=False)
        task.res = res.BaseRes(r, request.isParseRes)
        return task

    def Get(self, task):
        request = task.req
        if request.params == None:
            request.params = {}

        if request.headers == None:
            request.headers = {}

        r = self.session.get(request.url, proxies=request.proxy, headers=request.headers, timeout=task.timeout, verify=False)
        task.res = res.BaseRes(r, request.isParseRes)
        return task

    def Download(self, request, token="", backParams="", cacheAndLoadPath="", loadPath= "", isASync=True):
        self.__DealHeaders(request, token)
        task = Task(request, backParams, cacheAndLoadPath, loadPath)
        if isASync:
            self._downloadQueue.put(task)
        else:
            self._Download(task)

    def _Download(self, task):
        try:
            for cachePath in [task.cacheAndLoadPath, task.loadPath]:
                if cachePath and task.backParam:
                    data = ToolUtil.LoadCachePicture(cachePath)
                    if data:
                        from src.qt.util.qttask import QtTask
                        QtTask().downloadBack.emit(task.backParam, len(data), data)
                        QtTask().downloadBack.emit(task.backParam, 0, b"")
                        return
            request = task.req
            if request.params == None:
                request.params = {}

            if request.headers == None:
                request.headers = {}

            Log.Info("request-> backId:{}, {}".format(task.backParam, task.req))
            r = self.session.get(request.url, proxies=request.proxy, headers=request.headers, stream=True, timeout=task.timeout, verify=False)
            # task.res = res.BaseRes(r)
            task.res = r
        except Exception as es:
            Log.Warn(task.req.url + " " + es.__repr__())
            task.status = Status.NetError
        self.handler.get(task.req.__class__)(task)
        if task.res:
            task.res.close()

    def TestSpeedPing(self, request, backParams=""):
        self.__DealHeaders(request, "")
        task = Task(request, backParams)
        self._inQueue.put(task)
