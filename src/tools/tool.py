import json
import os
import re
import time
from urllib.parse import quote

from bs4 import BeautifulSoup, Tag

from config import config
from config.setting import Setting
from tools.log import Log
from tools.status import Status


class CTime(object):
    def __init__(self):
        self._t1 = time.time()

    def Refresh(self, clsName, des='', checkTime=100):
        t2 = time.time()
        diff = int((t2 - self._t1) * 1000)
        if diff >= checkTime:
            text = 'CTime consume:{} ms, {}.{}'.format(diff, clsName, des)
            Log.Warn(text)
        self._t1 = t2
        return diff


def time_me(fn):
    def _wrapper(*args, **kwargs):
        start = time.time()
        rt = fn(*args, **kwargs)
        diff = int((time.time() - start) * 1000)
        if diff >= 100:
            clsName = args[0]
            strLog = 'time_me consume,{} ms, {}.{}'.format(diff, clsName, fn.__name__)
            # Log.w(strLog)
            Log.Warn(strLog)
        return rt

    return _wrapper


class ToolUtil(object):
    Category = dict()
    Category["doujinshi"] = "同人志"
    Category["manga"] = "漫画"
    Category["artist cg"] = "艺术CG"
    Category["game cg"] = "游戏CG"
    Category["western"] = "西方"
    Category["non-h"] = "无H"
    Category["image set"] = "图集"
    Category["cosplay"] = "COSPLAY"
    Category["asian porn"] = "亚洲色情"
    Category["misc"] = "杂项"

    @staticmethod
    def GetCategoryName(category):
        if Setting.Language.autoValue != 3:
            return ToolUtil.Category.get(category.lower())
        return category

    @classmethod
    def GetHeader(cls, _url: str, method: str) -> dict:
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        }
        if Setting.Language.autoValue == 1:
            header["Accept-Language"] = "zh-CN,zh;q=0.9"
        elif Setting.Language.autoValue == 3:
            header["Accept-Language"] = "en-US,en;q=0.9"
        else:
            header["Accept-Language"] = "zh-HK,zh;q=0.9"
        return header

    @staticmethod
    def DictToUrl(paramDict):
        assert isinstance(paramDict, dict)
        data = ''
        for k, v in paramDict.items():
            data += quote(str(k)) + '=' + quote(str(v))
            data += '&'
        return data.strip('&')

    @staticmethod
    def ParseFromData(desc, src):
        try:
            if not src:
                return
            if isinstance(src, str):
                src = json.loads(src)
            for k, v in src.items():
                setattr(desc, k, v)
        except Exception as es:
            Log.Error(es)

    @staticmethod
    def GetUrlHost(url):
        host = url.replace("https://", "")
        host = host.replace("http://", "")
        host = host.split("/")[0]
        host = host.split(":")[0]
        return host

    @staticmethod
    def GetDateStr(createdTime):
        timeArray = time.strptime(createdTime, "%Y-%m-%dT%H:%M:%S.%f%z")
        tick = int(time.mktime(timeArray) - time.timezone)
        now = int(time.time())
        day = int((int(now - time.timezone) / 86400) - (int(tick - time.timezone) / 86400))
        return time.localtime(tick), day

    @staticmethod
    def GetUpdateStr(createdTime):
        timeArray = time.strptime(createdTime, "%Y-%m-%dT%H:%M:%S.%f%z")
        now = int(time.time())
        tick = int(time.mktime(timeArray) - time.timezone)
        day = (now - tick) // (24 * 3600)
        hour = (now - tick) // 3600
        minute = (now - tick) // 60
        second = (now - tick)
        if day > 0:
            return "{}天前".format(day)
        elif hour > 0:
            return "{}小时前".format(hour)
        elif minute > 0:
            return "{}分钟前".format(minute)
        else:
            return "{}秒前".format(second)

    @staticmethod
    def GetDownloadSize(downloadLen):
        kb = downloadLen / 1024.0
        if kb <= 0.1:
            size = str(downloadLen) + "bytes"
        else:
            mb = kb / 1024.0
            if mb <= 0.1:
                size = str(round(kb, 2)) + "kb"
            else:
                size = str(round(mb, 2)) + "mb"
        return size

    @staticmethod
    def GetLookScaleModel(category, mat="jpg"):
        return ToolUtil.GetModelByIndex(Setting.LookNoise.value, Setting.LookScale.value, ToolUtil.GetLookModel(category), mat)

    @staticmethod
    def GetDownloadScaleModel(w, h, mat):
        dot = w * h
        # 条漫不放大
        if not config.CanWaifu2x:
            return {}
        return ToolUtil.GetModelByIndex(Setting.DownloadNoise.value, Setting.DownloadScale.value, Setting.DownloadModel.value, mat)

    @staticmethod
    def GetPictureSize(data):
        if not data:
            return 0, 0, "jpg"
        from PIL import Image
        from io import BytesIO
        a = BytesIO(data)
        img = Image.open(a)
        a.close()
        if img.format == "PNG":
            mat = "png"
        else:
            mat = "jpg"
        return img.width, img.height, mat

    @staticmethod
    def GetLookModel(category):
        if Setting.LookModel.value == 0:
            if "Cosplay" in category or "cosplay" in category or "CosPlay" in category or "COSPLAY" in category:
                return 2
            return 3
        else:
            return Setting.LookModel.value

    @staticmethod
    def GetModelAndScale(model):
        if not model:
            return "cunet", 1, 1
        index = model.get('index', 0)
        scale = model.get('scale', 0)
        noise = model.get('noise', 0)
        if index == 0:
            model = "anime_style_art_rgb"
        elif index == 1:
            model = "cunet"
        elif index == 2:
            model = "photo"
        else:
            model = "anime_style_art_rgb"
        return model, noise, scale

    @staticmethod
    def GetModelByIndex(noise, scale, index, mat="jpg"):
        if not config.CanWaifu2x:
            return {}
        if noise < 0:
            noise = 3
        data = {"format": mat, "noise": noise, "scale": scale, "index": index}
        from waifu2x_vulkan import waifu2x_vulkan
        if index == 0:
            data["model"] = getattr(waifu2x_vulkan, "MODEL_ANIME_STYLE_ART_RGB_NOISE"+str(noise))
        elif index == 1:
            data["model"] = getattr(waifu2x_vulkan, "MODEL_CUNET_NOISE"+str(noise))
        elif index == 2:
            data["model"] = getattr(waifu2x_vulkan, "MODEL_PHOTO_NOISE" + str(noise))
        elif index == 3:
            data["model"] = getattr(waifu2x_vulkan, "MODEL_ANIME_STYLE_ART_RGB_NOISE"+str(noise))
        else:
            data["model"] = getattr(waifu2x_vulkan, "MODEL_CUNET_NOISE"+str(noise))
        return data

    @staticmethod
    def GetCanSaveName(name):
        return re.sub('[\\\/:*?"<>|\0\r\n]', '', name).rstrip(".").strip(" ")

    @staticmethod
    def LoadCachePicture(filePath):
        try:
            c = CTime()
            if not os.path.isfile(filePath):
                return None
            with open(filePath, "rb") as f:
                data = f.read()
                c.Refresh("LoadCache", filePath)
                return data
        except Exception as es:
            Log.Error(es)
        return None

    @staticmethod
    def IsHaveFile(filePath):
        try:
            if os.path.isfile(filePath):
                return True
            return False
        except Exception as es:
            Log.Error(es)
        return False

    @staticmethod
    def DiffDays(d1, d2):
        return (int(d1 - time.timezone) // 86400) - (int(d2 - time.timezone) // 86400)

    @staticmethod
    def GetCurZeroDatatime(tick):
        from datetime import timedelta
        from datetime import datetime
        now = datetime.fromtimestamp(tick)
        delta = timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
        zeroDatetime = now - delta
        return int(time.mktime(zeroDatetime.timetuple()))

    @staticmethod
    def GetTimeTickEx(strDatetime):
        if not strDatetime:
            return 0
        timeArray = time.strptime(strDatetime, "%Y-%m-%d %H:%M:%S")
        tick = int(time.mktime(timeArray))
        return tick

    @staticmethod
    def ParseBookIndex(data):
        soup = BeautifulSoup(data, features="lxml")
        tag = soup.find("table", class_=re.compile(r"itg gl\w+"))
        bookInfos = []
        if not tag:
            return [], 1
        for tr in tag.children:
            from tools.book import BookInfo
            info = BookInfo()
            baseInfo = info.baseInfo
            for td in tr.children:
                className = " ".join(td.attrs.get('class', []))
                if className == "gl1c glcat":
                    baseInfo.category = td.text
                elif className == "gl2c":
                    bookInfos.append(info)
                    picture = td.find("img")
                    baseInfo.title = picture.attrs.get("title")
                    url = picture.attrs.get("data-src")
                    if url:
                        baseInfo.imgUrl = url
                        baseInfo.imgData = picture.attrs.get("src")
                    else:
                        baseInfo.imgUrl = picture.attrs.get("src")

                    timeTag = td.find("div", id=re.compile(r"postedpop_\d+"))
                    baseInfo.id = re.findall(r"\d+", timeTag.attrs.get("id"))[0]
                    baseInfo.timeStr = timeTag.text
                elif className == "gl3c glname":
                    baseInfo.bookUrl = td.next.attrs.get("href")
                    for tag in td.find_all("div", class_="gt"):
                        baseInfo.tags.append(tag.attrs.get("title"))

                    pass
                elif className == "gl4c glhide":
                    pass
            mo = re.search("(?<={}/)\w*".format(baseInfo.id), baseInfo.bookUrl)
            if mo:
                baseInfo.token = mo.group()

        table = soup.find("table", class_="ptt")
        maxPage = 1
        for td in table.tr.children:
            if getattr(td, "a", None):
                pages = td.a.text
                datas = re.findall(r"\d+", pages)
                if not datas:
                    continue
                maxPage = max(maxPage, int(datas[0]))
        return bookInfos, maxPage

    @staticmethod
    def ParseBookInfo(data):
        soup = BeautifulSoup(data, features="lxml")
        tag = soup.find("div", id="gdd")
        table = tag.find("table")
        from tools.book import BookInfo
        book = BookInfo()
        info = book.pageInfo
        for tr in table.find_all("tr"):
            key = tr.find("td", class_="gdt1").text.replace(":", "")
            value = tr.find("td", class_="gdt2").text
            info.kv[key] = value
        info.posted = info.kv.get("Posted")
        info.language = info.kv.get("Language")
        info.fileSize = info.kv.get("File Size")
        mo = re.search(r'\d+', info.kv.get("Length"))
        if mo:
            info.pages = int(mo.group())
        mo = re.search(r"\d+", info.kv.get("Favorited", ""))
        if mo:
            info.favorites = int(mo.group())

        for tag in soup.find_all("div", class_=re.compile("gdt\w")):
            url = tag.a.attrs.get('href')
            index = int(tag.a.img.attrs.get('alt'))
            info.picUrl[index] = url

        table = soup.find("table", class_="ptt")
        maxPage = 1
        for td in table.tr.children:
            if getattr(td, "a", None):
                pages = td.a.text
                datas = re.findall(r"\d+", pages)
                if not datas:
                    continue
                maxPage = max(maxPage, int(datas[0]))

        comment = soup.find("div", id="cdiv")
        for tag in comment.find_all("div", class_="c1"):
            times = tag.find("div", class_="c3").text
            data = tag.find("div", class_="c6").text
            info.comment.append([times, data])
        base = book.baseInfo
        data = soup.find_all("script", {'type': "text/javascript"})
        mo = re.search("(?<=var gid =\s)\d+", data[1].next)
        base.id = mo.group()
        mo = re.search("(?<=var token = \")\w+", data[1].next)
        base.token = mo.group()
        mo = re.search("(?<=var apiuid = )\S*(?=;)", data[1].next)
        base.apiUid = mo.group()
        mo = re.search("(?<=var apikey = \")\w+", data[1].next)
        base.apiKey = mo.group()
        mo = re.search("(?<=var average_rating =\s)\d+(.\d+)", data[1].next)
        base.average_rating = mo.group()
        mo = re.search("(?<=var display_rating =\s)\d+(.\d+)", data[1].next)
        base.display_rating = mo.group()
        tag = soup.find("div", id="gdc")
        base.category = tag.text.replace("\n", "")
        tag = soup.find("h1", id="gn")
        base.title = tag.text
        tag = soup.find("div", id="gd1")
        base.imgUrl = re.search("(?<=url\()\S*(?=\))", tag.div.attrs.get("style")).group()
        table = soup.find("div", id="taglist")
        for tc in table.find_all("td", class_="tc"):
            td = tc.find_next_sibling()
            if td:
                for div in td.find_all("div"):
                    base.tags.append(tc.text + div.text)

        tag = soup.find("p", class_="br")
        commentError = ""
        if tag:
            commentError = tag.text
        return book, maxPage, commentError

    @staticmethod
    def ParsePictureInfo(data):
        soup = BeautifulSoup(data, features="lxml")
        tag = soup.find("div", id="i3")
        imgUrl = tag.a.img.attrs.get("src")
        mo = re.search("(?<=showkey)(\s*=\s*\")\w+", data)
        imgKey = mo.group().replace("\"", "").replace("=", "").replace(" ", "")
        return imgUrl, imgKey

    @staticmethod
    def ParsePictureInfo2(data):
        data = json.loads(data)
        tag = data.get('i3')
        mo = re.search("(?<=src=\")\S+(?=\")", str(tag))
        if not mo:
            return ""
        imgUrl = mo.group().replace("\\/", "/")
        return imgUrl

    @staticmethod
    def MergeUrlParams(url, data: dict):
        if not data:
            return url
        if url[-1] != "/":
            url += "/?"
        for key, value in data.items():
            url += "{}={}".format(key, value)
            url += "&"
        return url.strip("&")

    # 解析添加收藏
    @staticmethod
    def ParseAddFavorite(data):
        soup = BeautifulSoup(data, features="lxml")
        tag = soup.find("textarea")
        note = tag.text
        table = soup.find_all("input")
        favorite = {}
        isUpdate = False
        for tr in table:
            if tr.attrs.get("type") == "radio":
                favorite[tr.attrs.get("value")] = tr.attrs.get("checked") == "checked"
            elif tr.attrs.get("type") == "submit":
                if tr.attrs.get("value") == "Apply Changes":
                    isUpdate = True
        return note, favorite, isUpdate

    # 解析添加收藏夹
    @staticmethod
    def ParseFavorite(data):
        soup = BeautifulSoup(data, features="lxml")
        table = soup.find_all("div", class_="fp")
        favorite = {}
        for index, tr in enumerate(table):
            count = 0
            for tag in tr.children:
                if isinstance(tag, Tag):
                    if len(tag.attrs) == 1 and tag.attrs.get("style"):
                        mo = re.search(r"\d+", tag.text)
                        if mo:
                            count = int(mo.group())
                            break

            favorite[index] = count
        return favorite

    @staticmethod
    def ParseLoginUserName(data):
        soup = BeautifulSoup(data, features="lxml")
        table = soup.find("div", id="userlinks")
        if not table:
            return "", ""
        tag = table.find("a")
        if not tag:
            return "", ""
        name = tag.text
        userId = "", ""
        mo = re.search("(?<=showuser=)\w+", tag.attrs.get("href", ""))
        if mo:
            userId = mo.group()
        return userId, name

    @staticmethod
    def ParseLoginResult(data):
        soup = BeautifulSoup(data, features="lxml")
        table = soup.find("div", class_="tablepad")
        if not table:
            return Status.Error
        if "captcha" in table.text:
            return Status.NeedGoogle
        elif "password incorrect" in table.text:
            return Status.UserError
        return Status.Error

    @staticmethod
    def ParseHomeInfo(data):
        soup = BeautifulSoup(data, features="lxml")
        tag = soup.find("div", class_="homebox")
        # print(tag.text)
        mo = re.search("(?<=You are currently at\s)\d*", tag.text)
        curNum = 0
        if mo:
            curNum = int(mo.group())
        mo = re.search("(?<=towards a limit of\s)\d*", tag.text)
        maxNum = 0
        if mo:
            maxNum = int(mo.group())
        return curNum, maxNum