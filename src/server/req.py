import json

from conf import config
from src.util import ToolUtil


class ServerReq(object):
    def __init__(self, url, header=None, params=None, method="POST") -> None:
        self.url = url
        self.headers = header
        self.params = params
        self.method = method
        self.isParseRes = False
        self.proxy = {"http": config.HttpProxy, "https": config.HttpProxy}


# 下载图片
class DownloadBookReq(ServerReq):
    def __init__(self, url, path="", isSaveCache=False):
        method = "Download"
        self.url = url
        self.path = path
        self.isSaveCache = isSaveCache
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 登陆
class LoginReq(ServerReq):
    def __init__(self, userId, passwd):
        method = "POST"
        url = config.FormUrl + "/index.php?act=Login&CODE=01"

        header = ToolUtil.GetHeader(url, method)
        header["Referer"] = config.Url + "/bounce_login.php?b=d&bt=1-1"
        header["Sec-Fetch-Dest"] = "document"
        header["Sec-Fetch-Mode"] = "navigate"
        header["Sec-Fetch-Site"] = "same-site"
        header["Sec-Fetch-User"] = "?1"
        header["Upgrade-Insecure-Requests"] = "1"
        header["Origin"] = config.Url
        header["Content-Type"] = "application/x-www-form-urlencoded"

        data = dict()
        data["CookieDate"] = "1"
        data["b"] = "d"
        data["bt"] = "1-1"
        data["UserName"] = userId
        data["PassWord"] = passwd
        data["ipb_login_submit"] = "Login!"
        super(self.__class__, self).__init__(url, header, ToolUtil.DictToUrl(data), method)


# 获得Home
class HomeReq(ServerReq):
    def __init__(self):
        method = "GET"
        url = config.Url + "/home.php"

        header = ToolUtil.GetHeader(url, method)
        data = dict()
        super(self.__class__, self).__init__(url, header, data, method)


# 获得UserId
class GetUserIdReq(ServerReq):
    def __init__(self):
        method = "GET"
        url = config.FormUrl + "/index.php?"

        header = ToolUtil.GetHeader(url, method)
        data = dict()
        super(self.__class__, self).__init__(url, header, data, method)


# 检查更新
class CheckUpdateReq(ServerReq):
    def __init__(self, url):
        # url = config.UpdateUrl
        method = "GET"
        super(self.__class__, self).__init__(url, {}, {}, method)
        self.isParseRes = False


# 本子信息
class BookInfoReq(ServerReq):
    def __init__(self, bookId, page=1):
        from src.book.book import BookMgr
        info = BookMgr().GetBook(bookId)
        self.bookId = bookId
        self.page = page
        url = info.baseInfo.bookUrl

        params = dict()
        if page > 1:
            params["p"] = str(page - 1)
        else:
            params["nw"] = "always"
        data = ToolUtil.DictToUrl(params)
        if data:
            url += "/?" + data
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method), {}, method)


# 图片信息
class GetBookImgUrl(ServerReq):
    def __init__(self, bookId, index):
        from src.book.book import BookMgr
        info = BookMgr().GetBook(bookId)
        self.bookId = bookId
        self.index = index
        url = info.pageInfo.picUrl.get(index)
        method = "Get"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method), {}, method)


# 图片信息Api
class GetBookImgUrl2(ServerReq):
    def __init__(self, bookId, index):
        self.bookId = bookId
        self.index = index
        from src.book.book import BookMgr
        info = BookMgr().GetBook(bookId)
        url = config.ApiUrl
        method = "POST"
        data = {
            'gid': self.bookId,
            'imgkey': info.pageInfo.GetImgKey(index),
            'method': 'showpage',
            'page': self.index,
            'showkey': info.pageInfo.showKey
        }
        header = ToolUtil.GetHeader(url, method)
        header["Content-Type"] = "application/json; charset=UTF-8"
        super(self.__class__, self).__init__(url, header, json.dumps(data), method)


# 获得首页
class GetIndexInfoReq(ServerReq):
    def __init__(self, page=1, f_search=""):
        url = config.Url
        data = {}
        if page > 1:
            data['page'] = str(page - 1)

        if f_search:
            data['f_search'] = str(f_search)
        data["inline_set"] = "dm_l"
        param = ToolUtil.DictToUrl(data)
        if param:
            url += "/?" + param
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 获得收藏
class GetFavoritesReq(ServerReq):
    def __init__(self, favcat="", page=1):
        url = config.Url + "/favorites.php"
        data = {}
        if page > 1:
            data['page'] = str(page - 1)
        else:
            data["nw"] = "always"
        if favcat != "":
            data["favcat"] = str(favcat)
        param = ToolUtil.DictToUrl(data)
        if param:
            url += "/?" + param
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 添加收藏
class AddFavoritesReq(ServerReq):
    def __init__(self, bookId=""):
        from src.book.book import BookMgr
        info = BookMgr().GetBook(bookId)
        url = config.Url + "/gallerypopups.php?gid={}&t={}&act=addfav".format(bookId, info.baseInfo.token)
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 添加收藏2
class AddFavorites2Req(ServerReq):
    def __init__(self, bookId="", favcat=0, msg="", isUpdate=False):
        from src.book.book import BookMgr
        info = BookMgr().GetBook(bookId)
        url = config.Url + "/gallerypopups.php?gid={}&t={}&act=addfav".format(bookId, info.baseInfo.token)
        method = "POST"
        header = ToolUtil.GetHeader(url, method)
        header["content-type"] = "application/x-www-form-urlencoded"

        data = dict()
        data["favcat"] = favcat
        data["favnote"] = msg
        data["update"] = "1"
        if isUpdate:
            data["apply"] = "Apply Changes"
        else:
            data["apply"] = "Add to Favorites"
        super(self.__class__, self).__init__(url, header,
                                             ToolUtil.DictToUrl(data), method)


# 删除收藏
class DelFavoritesReq(ServerReq):
    def __init__(self, bookId=""):
        url = config.Url + "/favorites.php"
        method = "POST"

        header = ToolUtil.GetHeader(url, method)
        header["content-type"] = "application/x-www-form-urlencoded"
        data = dict()
        data["modifygids[]"] = bookId
        data["apply"] = "Confirm"
        data["ddact"] = "delete"
        super(self.__class__, self).__init__(url, header,
                                             ToolUtil.DictToUrl(data), method)