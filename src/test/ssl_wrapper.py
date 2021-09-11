"""
Provides x509 certificates and paths.
"""

from os import mkdir
from os.path import abspath, dirname, isdir, isfile, join
import OpenSSL.crypto as crypto


proxy_CN = 'proxy2 CA'

# TODO: do this on package-install-time after move to pyopenssl
# dir_name = join(dirname(abspath(__file__)), 'ssl-data')
dir_name = "ssl-data"

ca_key = join(dir_name, 'ca.key')
ca_crt = join(dir_name, 'ca.crt')
cert_key = join(dir_name, 'cert.key')
cert_dir = join(dir_name, 'certs')

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


def create_cert_request(p_key, digest="sha256", **subject_kwargs):
    """
    Creates certificate request
    :param p_key: key to associate with the request
    :param digest: signing method
    :param subject_kwargs: subject of request
        valuable args are: (took from RFC 5280)
          C:    country
          ST:   state or province name
          L:    Locality name
          O:    organization
          OU:   organizational unit
          CN:   common name (e.g., "Susan Housley")
          emailAddress: e-mail
    :return: certificate request
    """
    req = crypto.X509Req()
    subj = req.get_subject()

    for key, value in subject_kwargs.items():
        setattr(subj, key, value)

    req.set_pubkey(p_key)
    req.sign(p_key, digest)
    return req


def create_certificate(
        req, cert_key_pair, serial, begin_end_validity, digest="sha256",
        self_signed_x509v3=False, subject_alt_names=[]):
    """
    Create certificate by certificate request.
    :param req: certificate request
    :param cert_key_pair: tuple with issuer certificate and private key
    :param serial: serial number
    :param begin_end_validity: tuple with seconds certificate validity.
      0 means now. Example for set one year valid certificate from now:
      begin_end_validity=(0, 60*60*24*365)
    :param digest: signing method
    :param self_signed_x509v3: generate self signed x509v3 CA certificate, add
     extensions similar to these:
      X509v3 extensions:
           X509v3 Subject Key Identifier:
               88:31:6A:B7:8C:B3:F0:1D:5F:CD:9F:F8:70:F7:D4:7C:E5:5E:D2:A1
           X509v3 Authority Key Identifier:
               keyid:88:31:6A:B7:8C:B3:F0:1D:5F:CD:9F:F8:70:F7:D4:7C:E5:5E:D2:A1
           X509v3 Basic Constraints:
               CA:TRUE
    :param subject_alt_names: subject alt names e.g. IP:192.168.7.1 or DNS:my.domain
    :return: signed certificate
    :return type: crypto.X509
    """
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


def ca_files_exist():
    return all(
        list(map(isfile, [ca_key, ca_crt, cert_key])) + [isdir(dir_name)])

if not ca_files_exist():
    # TODO: move this code to pyopenssl library
    try:
        if not isdir(dir_name):
            mkdir(dir_name)
        ca_key_o = generate_key_pair(crypto.TYPE_RSA, 2048)
        cert_key_o = generate_key_pair(crypto.TYPE_RSA, 2048)
        cert_req_temp = create_cert_request(ca_key_o, CN=proxy_CN)
        ca_crt_o = create_certificate(
            cert_req_temp, ('__self_signed', ca_key_o), 1509982490957715,
            (0, 60 * 60 * 24 * 30), self_signed_x509v3=True
        )
        with open(ca_key, 'wb+') as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, ca_key_o))
        with open(cert_key, 'wb+') as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, cert_key_o))
        with open(ca_crt, 'wb+') as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, ca_crt_o))

        if not isdir(cert_dir):
            mkdir(cert_dir)

    except StandardError as e:
        logger.exception(e)


def _load_crypto_obj(path, crypto_method):
    with open(path, 'r') as key_fp:
        return crypto_method(crypto.FILETYPE_PEM, key_fp.read())

cert_key_obj = _load_crypto_obj(cert_key, crypto.load_privatekey)
ca_key_obj = _load_crypto_obj(ca_key, crypto.load_privatekey)
ca_crt_obj = _load_crypto_obj(ca_crt, crypto.load_certificate)


__all__ = [
    'proxy_CN',
    'dir_name',
    'ca_key',
    'ca_crt',
    'cert_key',
    'cert_dir',
    'ca_files_exist',
    'cert_key_obj',
    'ca_key_obj',
    'ca_crt_obj',
    'generate_key_pair',
    'create_cert_request',
    'create_certificate',
]


if __name__ == '__main__':
    def _load_crypto_obj(path, crypto_method):
        with open(path, 'r') as key_fp:
            return crypto_method(crypto.FILETYPE_PEM, key_fp.read())

    cert_key_obj = _load_crypto_obj(cert_key, crypto.load_privatekey)
    ca_key_obj = _load_crypto_obj(ca_key, crypto.load_privatekey)
    ca_crt_obj = _load_crypto_obj(ca_crt, crypto.load_certificate)
    cert_req = create_cert_request(ca_key_obj, CN=proxy_CN)
    signed_req = create_certificate(
        cert_req, (ca_crt_obj, ca_key_obj), 1509982490957715,
        (0, 60 * 60 * 24 * 30), self_signed_x509v3=True
    )


    print(crypto.dump_certificate(crypto.FILETYPE_PEM, signed_req))
    'openssl x509 -req -days 3650 -CA ca.crt -CAkey ca.key -set_serial 1509982490957715'
    'https://github.com/pyca/pyopenssl/blob/master/examples/certgen.py'