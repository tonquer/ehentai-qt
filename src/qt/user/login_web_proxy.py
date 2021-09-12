import sys
import os
import socket
import ssl
import select
import threading
import gzip
import zlib
import time
import json
import re
from os.path import join, isdir
from string import Template
from OpenSSL import crypto
import http.client as httplib
import urllib.parse as urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from io import BytesIO

from conf import config
from src.util import Log


dns_hosts = {}
dir_name = "ssl-data"

ca_key = join(dir_name, 'ca.key')
ca_crt = join(dir_name, 'ca.crt')
cert_key = join(dir_name, 'cert.key')
cert_dir = join(dir_name, 'certs')


def print_color(c, s):
    print("\x1b[{}m{}\x1b[0m".format(c, s))

cert_key_obj = None
ca_key_obj = None
ca_crt_obj = None


def join_with_script_dir(path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)


def create_certificate(
        req, cert_key_pair, serial, begin_end_validity, digest="sha256",
        self_signed_x509v3=False, subject_alt_names=[]):
    i_cert, i_key = cert_key_pair
    not_before, not_after = begin_end_validity
    ret_x509_obj = crypto.X509()
    ret_x509_obj.set_serial_number(serial)

    ret_x509_obj.gmtime_adj_notAfter(not_after)
    ret_x509_obj.gmtime_adj_notBefore(not_before)
    if i_cert == '__self_signed':
        i_cert = ret_x509_obj
    ret_x509_obj.set_issuer(i_cert.get_subject())
    ret_x509_obj.set_subject(req.get_subject())
    ret_x509_obj.set_pubkey(req.get_pubkey())
    if self_signed_x509v3:
        ret_x509_obj.set_version(2)
        ret_x509_obj.add_extensions([
            crypto.X509Extension(b'subjectKeyIdentifier', False, b'hash',
                                 subject=ret_x509_obj),
            crypto.X509Extension(b'basicConstraints', False, b'CA:TRUE'),
            ])
        ret_x509_obj.add_extensions([
            crypto.X509Extension(b'authorityKeyIdentifier', False,
                                 b'keyid:always', issuer=ret_x509_obj),
        ])
    if len(subject_alt_names) != 0:
        ret_x509_obj.set_version(2) # 0x3
        ret_x509_obj.add_extensions([
            crypto.X509Extension(
                type_name=b'subjectAltName',
                critical=False,
                value=", ".join(subject_alt_names).encode())
        ])

    ret_x509_obj.sign(i_key, digest)
    return ret_x509_obj

def create_cert_request(p_key, digest="sha256", **subject_kwargs):
    req = crypto.X509Req()
    subj = req.get_subject()

    for key, value in subject_kwargs.items():
        setattr(subj, key, value)

    req.set_pubkey(p_key)
    req.sign(p_key, digest)
    return req


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    address_family = socket.AF_INET
    daemon_threads = True

    def handle_error(self, request, client_address):
        # surpress socket/ssl related errors
        cls, e = sys.exc_info()[:2]
        if cls is socket.error or cls is BrokenPipeError or cls is ssl.SSLError:
            # BrokenPipeError is socket.error in Python2 and standalone error in Python3.
            # This is most frequently raised error  here.
            # I don't understand why it raises here
            # looks like it is caused by some errors in the proxy logic: for some
            # reasons  a client closes connection
            # I thinks the keep-alive logic should be checked.
            pass
        else:
            return HTTPServer.handle_error(self, request, client_address)


class ProxyRequestHandler(BaseHTTPRequestHandler):
    cakey = join_with_script_dir('ca.key')
    cacert = join_with_script_dir('ca.crt')
    certkey = join_with_script_dir('cert.key')
    certdir = join_with_script_dir('certs/')
    timeout = 5
    lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        self.tls = threading.local()
        self.tls.conns = {}

        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def log_error(self, format, *args):
        # surpress "Request timed out: timeout('timed out',)"
        if isinstance(args[0], socket.timeout):
            return

        self.log_message(format, *args)

    def do_CONNECT(self):
        self.connect_intercept()

    def connect_intercept(self):
        hostname = self.path.split(':')[0]
        ippat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
        cert_category = "DNS"
        if ippat.match(hostname):
            cert_category = "IP"

        certpath = "%s/%s.crt" % (cert_dir.rstrip('/'), hostname)

        with self.lock:
            if not os.path.isfile(certpath):
                x509_serial = int("%d" % (time.time() * 1000))
                valid_time_interval = (0, 60 * 60 * 24 * 365)
                cert_request = create_cert_request(cert_key_obj, CN=hostname)
                cert = create_certificate(
                    cert_request, (ca_crt_obj, ca_key_obj), x509_serial,
                    valid_time_interval,
                    subject_alt_names=[
                        Template("${category}:${hostname}").substitute(hostname=hostname, category=cert_category)
                    ]
                )
                with open(certpath, 'wb+') as f:
                    f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))


        self.wfile.write("{} {} {}\r\n".format(self.protocol_version, 200, 'Connection Established').encode('latin-1'))
        self.wfile.write(b'\r\n')

        self.connection = ssl.wrap_socket(self.connection,
                                          keyfile=cert_key,
                                          certfile=certpath,
                                          server_side=True)

        self.rfile = self.connection.makefile("rb", self.rbufsize)
        self.wfile = self.connection.makefile("wb", self.wbufsize)

        conntype = self.headers.get('Proxy-Connection', '')
        if self.protocol_version == "HTTP/1.1" and conntype.lower() != 'close':
            self.close_connection = 0
        else:
            self.close_connection = 1
            print("CONNECTION CLOSED 0")

    def connect_relay(self):
        address = self.path.split(':', 1)
        address[1] = int(address[1]) or 443
        try:
            s = socket.create_connection(address, timeout=self.timeout)
        except Exception as e:
            self.send_error(502)
            return
        self.send_response(200, 'Connection Established')
        self.end_headers()

        conns = [self.connection, s]
        self.close_connection = 0
        while not self.close_connection:
            rlist, wlist, xlist = select.select(conns, [], conns, self.timeout)
            if xlist or not rlist:
                break
            for r in rlist:
                other = conns[1] if r is conns[0] else conns[0]
                data = r.recv(8192)
                if not data:
                    self.close_connection = 1
                    print("CONNECTION CLOSED 2")
                    break
                other.sendall(data)

    def do_GET(self):
        if self.path == 'http://proxy2.test/':
            self.send_cacert()
            return

        req = self
        content_length = int(req.headers.get('Content-Length', 0))
        req_body = self.rfile.read(content_length) if content_length else None

        if req.path[0] == '/':
            if isinstance(self.connection, ssl.SSLSocket):
                req.path = "https://{}{}".format(req.headers['Host'], req.path)
            else:
                req.path = "http://{}{}".format(req.headers['Host'], req.path)

        req_body_modified = self.request_handler(req, req_body)
        if req_body_modified is False:
            self.send_error(403)
            return
        elif req_body_modified is not None:
            req_body = req_body_modified
            if 'Content-Length' in req.headers:
                del req.headers['Content-Length']
            req.headers['Content-Length'] = str(len(req_body))

        u = urlparse.urlsplit(req.path)
        scheme, netloc, path = u.scheme, u.netloc, (u.path + '?' + u.query if u.query else u.path)
        assert scheme in ('http', 'https')
        # netloc = "172.67.0.127"
        # if netloc:
            # if 'Host' in req.headers:
            #     del req.headers['Host']
            # req.headers['Host'] = netloc

        newHearder = self.filter_headers(req.headers)
        # 自定义dns解析
        global dns_hosts
        if netloc in dns_hosts:
            netloc = dns_hosts.get(netloc)
        elif config.Language != "English" and netloc == "www.google.com":
            netloc = "recaptcha.net"
            del newHearder["Host"]
            newHearder["Host"] = "recaptcha.net"
        setattr(req, 'headers', newHearder)

        try:
            origin = (scheme, netloc)
            if origin not in self.tls.conns:
                if scheme == 'https':
                    self.tls.conns[origin] = httplib.HTTPSConnection(netloc, timeout=self.timeout, context = ssl._create_unverified_context())
                else:
                    self.tls.conns[origin] = httplib.HTTPConnection(netloc, timeout=self.timeout)
            conn = self.tls.conns[origin]
            conn.request(self.command, path, req_body, dict(req.headers))
            res = conn.getresponse()

            version_table = {10: 'HTTP/1.0', 11: 'HTTP/1.1'}
            setattr(res, 'headers', res.msg)
            setattr(res, 'response_version', version_table[res.version])

            # support streaming
            if 'Content-Length' not in res.headers and 'no-store' in res.headers.get('Cache-Control', ''):
                self.response_handler(req, req_body, res, '')
                setattr(res, 'headers', self.filter_headers(res.headers))
                self.relay_streaming(res)
                #with self.lock:
                #    self.save_handler(req, req_body, res, '')
                return

            res_body = res.read().decode('latin-1')
        except Exception as e:
            if origin in self.tls.conns:
                del self.tls.conns[origin]
            self.send_error(502)
            return

        content_encoding = res.headers.get('Content-Encoding', 'identity')
        res_body_plain = self.decode_content_body(res_body.encode('latin-1'), content_encoding)

        res_body_modified = self.response_handler(req, req_body, res, res_body_plain)
        if res_body_modified is False:
            self.send_error(403)
            return
        elif res_body_modified is not None:
            res_body_plain = res_body_modified
            res_body = self.encode_content_body(res_body_plain, content_encoding)
            if 'Content-Length' in res.headers:
                del res.headers['Content-Length']
            res.headers['Content-Length'] = str(len(res_body))

        if 'Content-Length' not in res.headers:
            res.headers['Content-Length'] = str(len(res_body))

        setattr(res, 'headers', self.filter_headers(res.headers))

        self.wfile.write("{} {} {}\r\n".format(self.protocol_version, res.status, res.reason).encode('latin-1'))
        for k, v in res.headers.items():
            self.send_header(k, v)
        self.end_headers()
        if res_body:
            self.wfile.write(res_body.encode('latin-1'))
        self.wfile.flush()

        with self.lock:
            self.save_handler(req, req_body, res, res_body_plain)

    def relay_streaming(self, res):
        self.wfile.write("{} {} {}\r\n".format(self.protocol_version, res.status, res.reason)
                         .encode('latin-1', 'strinct'))
        for k, v in res.headers.items():
            self.send_header(k, v)
        self.end_headers()
        try:
            while True:
                chunk = res.read(8192)
                if not chunk:
                    break
                self.wfile.write(chunk)
            self.wfile.flush()
        except socket.error:
            # connection closed by client
            pass

    do_HEAD = do_GET
    do_POST = do_GET
    do_PUT = do_GET
    do_DELETE = do_GET
    do_OPTIONS = do_GET

    def filter_headers(self, headers):
        # http://tools.ietf.org/html/rfc2616#section-13.5.1
        hop_by_hop = (
            'connection',
            'keep-alive',
            'proxy-authenticate',
            'proxy-authorization',
            'te',
            'trailers',
            'transfer-encoding',
            'upgrade'
        )
        for k in hop_by_hop:
            del headers[k]

        # accept only supported encodings
        if 'Accept-Encoding' in headers:
            ae = headers['Accept-Encoding']
            filtered_encodings = [x for x in re.split(r',\s*', ae) if x in ('identity', 'gzip', 'x-gzip', 'deflate')]
            del headers['Accept-Encoding']
            headers['Accept-Encoding'] = ', '.join(filtered_encodings)

        return headers

    def encode_content_body(self, text, encoding):
        if encoding == 'identity':
            data = text
        elif encoding in ('gzip', 'x-gzip'):
            io = BytesIO()
            with gzip.GzipFile(fileobj=io, mode='wb') as f:
                f.write(text)
            data = io.getvalue()
        elif encoding == 'deflate':
            data = zlib.compress(text)
        else:
            raise Exception("Unknown Content-Encoding: {}".format(encoding))
        return data

    def decode_content_body(self, data, encoding):
        if encoding == 'identity':
            text = data
        elif encoding in ('gzip', 'x-gzip'):
            io = BytesIO(data)
            with gzip.GzipFile(fileobj=io) as f:
                text = f.read()
        elif encoding == 'deflate':
            try:
                text = zlib.decompress(data)
            except zlib.error:
                text = zlib.decompress(data, -zlib.MAX_WBITS)
        elif encoding == 'br': #Brotli
            return data
        else:
            raise Exception("Unknown Content-Encoding: {}".format(encoding))
        return text

    def send_cacert(self):
        with open(self.cacert, 'rb') as f:
            data = f.read()

        self.wfile.write("{} {} {}\r\n".format(self.protocol_version, 200, 'OK').encode('latin-1'))
        self.send_header('Content-Type', 'application/x-x509-ca-cert')
        self.send_header('Content-Length', len(data))
        self.send_header('Connection', 'close')
        self.end_headers()
        self.wfile.write(data)

    def print_info(self, req, req_body, res, res_body):
        def parse_qsl(s):
            return '\n'.join("{:<20} {}".format(k, v) for k, v in urlparse.parse_qsl(s, keep_blank_values=True))

        req_header_text = "{} {} {}\n{}".format(req.command, req.path, req.request_version, req.headers)
        res_header_text = "{} {} {}\n{}".format(res.response_version, res.status, res.reason, res.headers)

        print_color(33, req_header_text)

        u = urlparse.urlsplit(req.path)
        if u.query:
            query_text = parse_qsl(u.query)
            print_color(32, "==== QUERY PARAMETERS ====\n{}\n".format(query_text))

        cookie = req.headers.get('Cookie', '')
        if cookie:
            cookie = parse_qsl(re.sub(r';\s*', '&', cookie))
            print_color(32, "==== COOKIE ====\n{}\n".format(cookie))

        auth = req.headers.get('Authorization', '')
        if auth.lower().startswith('basic'):
            token = auth.split()[1].decode('base64')
            print_color(31, "==== BASIC AUTH ====\n{}\n".format(token))

        if req_body is not None:
            req_body_text = None
            content_type = req.headers.get('Content-Type', '')

            if content_type.startswith('application/x-www-form-urlencoded'):
                req_body_text = parse_qsl(req_body.decode('latin-1'))
            elif content_type.startswith('application/json'):
                try:
                    json_obj = json.loads(req_body)
                    json_str = json.dumps(json_obj, indent=2)
                    if json_str.count('\n') < 50:
                        req_body_text = json_str
                    else:
                        lines = json_str.splitlines()
                        req_body_text = "{}\n({} lines)".format('\n'.join(lines[:50]), len(lines))
                except ValueError:
                    req_body_text = req_body
            elif len(req_body) < 1024:
                req_body_text = req_body

            # if req_body_text:
            #     print_color(32, "==== REQUEST BODY ====\n{}\n".format(req_body_text))

        # print_color(36, res_header_text)

        # if hasattr(res.headers, 'getheaders'):
        #     cookies = res.headers.getheaders('Set-Cookie')
        # else:
        #     cookies = res.headers.get_all('Set-Cookie')
        # if cookies:
        #     cookies = '\n'.join(cookies)
        #     print_color(31, "==== SET-COOKIE ====\n{}\n".format(cookies))

        if res_body is not None:
            res_body_text = None
            content_type = res.headers.get('Content-Type', '')

            if content_type.startswith('application/json'):
                try:
                    json_obj = json.loads(res_body)
                    json_str = json.dumps(json_obj, indent=2)
                    if json_str.count('\n') < 50:
                        res_body_text = json_str
                    else:
                        lines = json_str.splitlines()
                        res_body_text = "{}\n({} lines)".format('\n'.join(lines[:50]), len(lines))
                except ValueError:
                    res_body_text = res_body
            elif content_type.startswith('text/html'):
                pass
                # m = re.search(r'<title[^>]*>\s*([^<]+?)\s*</title>', res_body.decode('latin-1'), re.I)
                # if m:
                #     print_color(32, "==== HTML TITLE ====\n{}\n".format(html.unescape(m.group(1))))
            elif content_type.startswith('text/') and len(res_body) < 1024:
                res_body_text = res_body

            # if res_body_text:
            #     print_color(32, "==== RESPONSE BODY ====\n{}\n".format(res_body_text))

    def request_handler(self, req, req_body):
        pass

    def response_handler(self, req, req_body, res, res_body):
        pass

    def save_handler(self, req, req_body, res, res_body):
        self.print_info(req, req_body, res, res_body)


def UpdateDns(domain, address):
    global dns_hosts
    if not address:
        if address  in dns_hosts:
            dns_hosts.pop(address)
    dns_hosts[domain] = address


def ClearDns():
    global dns_hosts
    dns_hosts.clear()

httpd = None
def Init():
    try:

        def generate_key_pair(key_type, bits):
            """
            Creates key pair
            :param key_type: one of crypto.TYPE_RSA or crypto.TYPE_DSA
            :param bits: key length
            :return: key pair in a PKey object
            :return type: instance of crypto.PKey
            """
            pkey = crypto.PKey()
            pkey.generate_key(key_type, bits)
            return pkey

        def _load_crypto_obj(path, crypto_method):
            with open(path, 'r') as key_fp:
                return crypto_method(crypto.FILETYPE_PEM, key_fp.read())

        if not isdir(dir_name):
            os.mkdir(dir_name)
        proxy_CN = 'proxy2 CA'
        ca_key_o = generate_key_pair(crypto.TYPE_RSA, 2048)
        cert_key_o = generate_key_pair(crypto.TYPE_RSA, 2048)
        cert_req_temp = create_cert_request(ca_key_o, CN=proxy_CN)
        ca_crt_o = create_certificate(
            cert_req_temp, ('__self_signed', ca_key_o), 1509982490957715,
            (0, 60 * 60 * 24 * 30), self_signed_x509v3=True
        )
        if not os.path.isfile(ca_key):
            with open(ca_key, 'wb+') as f:
                f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, ca_key_o))
        if not os.path.isfile(cert_key):
            with open(cert_key, 'wb+') as f:
                f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, cert_key_o))
        if not os.path.isfile(ca_crt):
            with open(ca_crt, 'wb+') as f:
                f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, ca_crt_o))

        if not isdir(cert_dir):
            os.mkdir(cert_dir)
        global cert_key_obj
        global ca_key_obj
        global ca_crt_obj
        cert_key_obj = _load_crypto_obj(cert_key, crypto.load_privatekey)
        ca_key_obj = _load_crypto_obj(ca_key, crypto.load_privatekey)
        ca_crt_obj = _load_crypto_obj(ca_crt, crypto.load_certificate)
        server_address = ('127.0.0.1', 0)

        ProxyRequestHandler.protocol_version = "HTTP/1.1"
        global httpd
        httpd = ThreadingHTTPServer(server_address, ProxyRequestHandler)

        sa = httpd.socket.getsockname()
        print("Serving HTTP Proxy on {} port {} ...".format(sa[0], sa[1]))
        httpd.server_activate()

        sa = httpd.socket.getsockname()
        from conf import config
        config.LocalProxyPort = sa[1]
        def Run():
            Log.Warn("Serving HTTP Proxy on {} port {} ...".format(sa[0], sa[1]))
            httpd.serve_forever()
            Log.Warn(("Serving end..."))

        thread = threading.Thread(target=Run)
        thread.setDaemon(True)
        thread.start()

    except Exception as e:
        Log.Error(e)

def Stop():
    global httpd
    httpd.shutdown()

__all__ = [
    "Init",
    "Stop",
    "UpdateDns",
    "ClearDns",
]