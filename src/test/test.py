import re

import requests
from bs4 import BeautifulSoup


class BookBaseInfo(object):
    def __init__(self):
        self.id = 0
        self.title = ""
        self.bookUrl = ""
        self.category = ""
        self.timeStr = ""
        self.imgData = None
        self.imgUrl = ""
        self.tags = []


class BookPageInfo(object):
    def __init__(self):
        self.kv = {}
        self.pages = 0


class BookInfo(object):
    def __init__(self):
        self.baseInfo = BookBaseInfo()
        self.pageInfo = BookPageInfo()


def ParseBookInfo(data):
    soup = BeautifulSoup(data, features="lxml")
    tag = soup.find("table", attrs={"class": re.compile(r"itg glt")})
    bookInfos = []
    for tr in tag.children:
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
    table = soup.find("table", class_="ptt")
    maxPage = 1
    for td in table.tr.children:
        if getattr(td, "a", None):
            pages = td.a.text
            datas = re.findall(r"\d+", pages)
            if not datas:
                continue
            maxPage = max(maxPage, int(datas[0]))
    return

def ParseBookInfo1(data):
    soup = BeautifulSoup(data, features="lxml")
    tag = soup.find("table", attrs={"class": re.compile(r"itg glt")})
    if tag.attrs.get("class") == "itg gltm":
        pass
    bookInfos = []
    for tr in tag.children:
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
    table = soup.find("table", class_="ptt")
    maxPage = 1
    for td in table.tr.children:
        if getattr(td, "a", None):
            pages = td.a.text
            datas = re.findall(r"\d+", pages)
            if not datas:
                continue
            maxPage = max(maxPage, int(datas[0]))
    return

def ParsePictureInfo(data):
    soup = BeautifulSoup(data, features="lxml")
    tag = soup.find("div", id="gdd")
    table = tag.find("table")
    for tr in table.find_all("tr"):
        key = tr.find("td", class_="gdt1").text.replace(":", "")
        value = tr.find("td", class_="gdt2").text
    for tag in soup.find_all("div", class_="gdtm"):
        url = tag.a.attrs.get('href')
        index = int(tag.a.img.attrs.get('alt'))

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



def ParseImgInfo(data):
    soup = BeautifulSoup(data, features="lxml")
    tag = soup.find("div", id="i3")
    imgUrl = tag.a.img.attrs.get("src")
    mo = re.search("(?<=showkey)(\s*=\s*\")\w+", "; var showkey = \"n1efkp39mtk\";")
    imgKey = mo.group().replace("\"", "").replace("=", "").replace(" ", "")
    return


def ParseImgInfo2(data):
    # soup = BeautifulSoup(data, features="lxml")
    # tag = soup.find("div", id="i3")
    # imgUrl = tag.a.img.attrs.get("src")
    # mo = re.search("(?<=showkey)(\s*=\s*\")\w+", "; var showkey = \"n1efkp39mtk\";")
    # imgKey = mo.group().replace("\"", "").replace("=", "").replace(" ", "")
    tag = data.get('i3')
    mo = re.search("(?<=src=\")\S+\"", tag)
    imgUrl = mo.group().replace("\\/", "/").replace("\"", "")
    return

if __name__ == "__main__":
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "zh-CN,zh;q=0.9,ja;q=0.8",
    }
    # r = requests.get("https://e-hentai.org", proxies={"https": "http://127.0.0.1:10809"})
    # r = requests.get("https://e-hentai.org", proxies={"https": "http://127.0.0.1:10809"})
    # data = {"p":3,"s":"s\/286edf5f6a\/1886873-3","n":"<div class=\"sn\"><a onclick=\"return load_image(1, '97316d4642')\" href=\"https:\/\/e-hentai.org\/s\/97316d4642\/1886873-1\"><img src=\"https:\/\/ehgt.org\/g\/f.png\" \/><\/a><a id=\"prev\" onclick=\"return load_image(2, '052d8a4730')\" href=\"https:\/\/e-hentai.org\/s\/052d8a4730\/1886873-2\"><img src=\"https:\/\/ehgt.org\/g\/p.png\" \/><\/a><div><span>3<\/span> \/ <span>52<\/span><\/div><a id=\"next\" onclick=\"return load_image(4, 'db30a6df2a')\" href=\"https:\/\/e-hentai.org\/s\/db30a6df2a\/1886873-4\"><img src=\"https:\/\/ehgt.org\/g\/n.png\" \/><\/a><a onclick=\"return load_image(52, '2b55577f5f')\" href=\"https:\/\/e-hentai.org\/s\/2b55577f5f\/1886873-52\"><img src=\"https:\/\/ehgt.org\/g\/l.png\" \/><\/a><\/div>","i":"<div>87570749_p0.jpg :: 1280 x 1868 :: 275.3 KB<\/div>","k":"286edf5f6a","i3":"<a onclick=\"return load_image(4, 'db30a6df2a')\" href=\"https:\/\/e-hentai.org\/s\/db30a6df2a\/1886873-4\"><img id=\"img\" src=\"https:\/\/bahkojr.xmgymbdvpsjz.hath.network:60000\/h\/846ecb60b17f755063916a26c238535975a710f7-281958-1280-1868-jpg\/keystamp=1618130700-04778f9774;fileindex=89518293;xres=1280\/87570749_p0.jpg\" style=\"height:1868px;width:1280px\" onerror=\"this.onerror=null; nl('26561-449480')\" \/><\/a>","i5":"<div class=\"sb\"><a href=\"https:\/\/e-hentai.org\/g\/1886873\/50f0a88e47\/\"><img src=\"https:\/\/ehgt.org\/g\/b.png\" referrerpolicy=\"no-referrer\" \/><\/a><\/div>","i6":" &nbsp; <img src=\"https:\/\/ehgt.org\/g\/mr.gif\" class=\"mr\" \/> <a href=\"https:\/\/e-hentai.org\/?f_shash=286edf5f6a9d5e0dbef1ea8a9f632bf83aaba7ca&amp;fs_from=87570749_p0.jpg+from+%5BPixiv%5D+sy4+%2834274728%29\">Show all galleries with this file<\/a>  &nbsp; <img src=\"https:\/\/ehgt.org\/g\/mr.gif\" class=\"mr\" \/> <a href=\"#\" onclick=\"prompt('Copy the URL below.', 'https:\/\/e-hentai.org\/r\/846ecb60b17f755063916a26c238535975a710f7-281958-1280-1868-jpg\/forumtoken\/1886873-3\/87570749_p0.jpg'); return false\">Generate a static forum image link<\/a>  &nbsp; <img src=\"https:\/\/ehgt.org\/g\/mr.gif\" class=\"mr\" \/> <a href=\"#\" id=\"loadfail\" onclick=\"return nl('26561-449480')\">Click here if the image fails loading<\/a> ","i7":" &nbsp; <img src=\"https:\/\/ehgt.org\/g\/mr.gif\" class=\"mr\" \/> <a href=\"https:\/\/e-hentai.org\/fullimg.php?gid=1886873&amp;page=3&amp;key=8dzvg9z9mtk\">Download original 2404 x 3508 5.99 MB source<\/a>","si":26561,"x":"1280","y":"1868"}
    f = open("test.html", "r", encoding="utf-8")
    data = f.read()
    f.close()
    ParseBookInfo(data)
    print()
    pass