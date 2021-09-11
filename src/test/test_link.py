'''
自定义DNS
'''
import socket

from urllib3.util import connection

from src.util import ToolUtil

# https://ehwiki.org/wiki/IPs
host_table = {
    # "www.baidu.com": "127.0.0.1",
    # "e-hentai.org": "31.13.95.18",
    # "e-hentai.org": "104.20.135.21",
    "forums.e-hentai.org": "104.20.134.21",
    "exhentai.org": "178.175.129.254",
    "e-hentai.org": "104.20.135.21",
}
_orig_create_connection = connection.create_connection


def _dns_resolver(host):
    if host in host_table:
        print("自定义DNS 解析被调用")
        return host_table[host]
    else:
        return host


def patched_create_connection(address, *args, **kwargs):
    host, port = address
    hostname = _dns_resolver(host)
    return _orig_create_connection((hostname, port), *args, **kwargs)


def injectDNS(hosts: dict = host_table):
    host_table.update(hosts)
    connection.create_connection = patched_create_connection


def recoverDNS():
    connection.create_connection = _orig_create_connection
    host_table.clear()


'''
取消SNI发送
'''
import urllib3
import urllib3.contrib.pyopenssl
# urllib3.disable_warnings(urllib3.exceptions.SNIMissingWarning)
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def unsendSNI():
    urllib3.contrib.pyopenssl.HAS_SNI = False
    urllib3.contrib.pyopenssl.inject_into_urllib3()


def sendSNI():
    urllib3.contrib.pyopenssl.HAS_SNI = True
    urllib3.contrib.pyopenssl.extract_from_urllib3()


'''
取消证书 hostname 验证
'''
import urllib3

_origin_match_hostname = urllib3.connection._match_hostname


def _match_hostname(cert, asserted_hostname):
    # print("_do_nothing")
    pass


def uncheck_hostname():
    urllib3.connection._match_hostname = _match_hostname


def check_hostname():
    urllib3.connection._match_hostname = _origin_match_hostname

# curl "https://cloudflare-dns.com/dns-query?name=forums.e-hentai.org&type=A" -H "accept:application/dns-json"

a = 0

def TestA(b=a):
    print(b)

if __name__ == '__main__':
    import requests
    requests.packages.urllib3.disable_warnings()
    # url = "https://e-hentai.org"
    headerUrl = "https://e-hentai.org"
    # headerUrl = "https://forums.e-hentai.org/index.php?act=Login&CODE=00"
    # headerUrl = "https://104.20.134.21"
    headerUrl = "https://e-hentai.org/g/2006156/1158af85ec"
    # headerUrl = "https://github.com"
    headerUrl = "https://e-hentai.org/g/2006453/9d2a15534d//?nw=always"
    header = ToolUtil.GetHeader(headerUrl, "GET")
    # header["Host"] = "e-hentai.org"

    # headerUrl = "https://104.20.134.21/index.php?act=Login&CODE=00"
    # header = {}
    # header["Host"] = "forums.e-hentai.org"
    # header["authorization"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MTI3NDRmNmE5NjAzY2ZlNGZiN2ZhMDAiLCJlbWFpbCI6InRvbnF1ZXI5OTYiLCJyb2xlIjoibWVtYmVyIiwibmFtZSI6InRvbnF1ZXI5OTYiLCJ2ZXJzaW9uIjoiMi4yLjEuMy4zLjQiLCJidWlsZFZlcnNpb24iOiI0NSIsInBsYXRmb3JtIjoiYW5kcm9pZCIsImlhdCI6MTYyOTk2NDUzMiwiZXhwIjoxNjMwNTY5MzMyfQ.kI__8k3oJZ553zOMKpuTKYxyjw_hMwpY10kNOv1QdWE"
    injectDNS()
    unsendSNI()
    # uncheck_hostname()
    # proxy = {"http":"http://127.0.0.1:8080", "https":"http://127.0.0.1:8080"}
    # r = requests.get(headerUrl, headers=header, proxies=proxy, timeout=5, verify=False)
    session = requests.session()
    # load_cookies = {
    #     "ipb_member_id": "6038327",
    #     "ipb_pass_hash": "8675cc310fbf3b710d0a4174fd6e07af",
    #     "igneous": "74dc6a88c"
    #     # "ipb_session_id": "d28b87796bcfacec89468a2cd7c7821b",
    # }
    # session.cookies = requests.utils.cookiejar_from_dict(load_cookies, cookiejar=None, overwrite=True)
    # headerUrl = "https://forums.e-hentai.org/index.php"
    # # proxy = {"http":"http://127.0.0.1:10809", "https":"http://127.0.0.1:10809"}
    proxy = {}
    # r = session.get(headerUrl, headers=header, proxies=proxy, timeout=5, verify=False)
    headerUrl = "https://e-hentai.org/s/dcded1d8b1/2007667-185"
    r = session.get(headerUrl, headers=header, proxies=proxy, timeout=5, verify=False)
    print(r.cookies)
    print(r.text)
    cookies = requests.utils.dict_from_cookiejar(r.cookies)
    igneous = cookies.get("igneous")
    print(igneous)
    # recoverDNS()
    # sendSNI()
    # check_hostname()