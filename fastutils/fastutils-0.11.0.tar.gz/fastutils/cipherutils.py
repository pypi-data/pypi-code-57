import base64
import binascii
from decimal import Decimal
from . import strutils
from . import randomutils
from . import aesutils
from .aesutils import get_md5_key as md5_key
from .aesutils import get_mysql_aes_key as mysql_aes_key
from .aesutils import get_sha1prng_key as sha1prng_key
from .aesutils import padding_ansix923 as aes_padding_ansix923
from .aesutils import padding_iso10126 as aes_padding_iso10126
from .aesutils import padding_pkcs5 as aes_padding_pkcs5


def get_s12_encode_map(password):
    v = randomutils.Random(password).get_bytes(256)
    values = list(range(256))
    delta = 0
    for index in range(256):
        delta += v[index]
        values[index] += delta
    return values

def get_s12_encode_bytes(password):
    encode_map = get_s12_encode_map(password)
    encode_bytes = {}
    for code in range(256):
        value = encode_map[code]
        high = value // 256
        low = value % 256
        encode_bytes[bytes([code])] = bytes([high, low])
    return encode_bytes

def get_s12_decode_bytes(password):
    encode_map = get_s12_encode_map(password)
    decode_bytes = {}
    for code in range(256):
        value = encode_map[code]
        high = value // 256
        low = value % 256
        decode_bytes[bytes([high, low])] = bytes([code])
    return decode_bytes

def s12_encrypt(data, password):
    data = strutils.force_bytes(data)
    encode_bytes = get_s12_encode_bytes(password)
    return b"".join([encode_bytes[bytes([code])] for code in data])

def s12_decrypt(data, password):
    result = b''
    decode_bytes = get_s12_decode_bytes(password)
    for start in range(0, len(data), 2):
        result += decode_bytes[data[start: start + 2]]
    return result

def get_iv_params(password):
    gen = randomutils.Random(password)
    n = gen.randint(9999, 1024)
    iv = [gen.randint(100, 1) for _ in range(n)]
    return n, iv

def iv_encrypt(number, password):
    number = strutils.force_int(number)
    flag = False
    if number < 0:
        number = -1 * number
        flag = True
    n, iv = get_iv_params(password)
    s = sum(iv)
    a = number // n
    b = number % n
    r = a * s + sum(iv[:b])
    if flag:
        r = -1 * r
    return r

def iv_decrypt(number, password):
    number = strutils.force_int(number)
    flag = False
    if number < 0:
        number = -1 * number
        flag = True
    n, iv = get_iv_params(password)
    s = sum(iv)
    a = number // s
    t = s * a
    if t == number:
        r = a * n
    else:
        for delta in range(n):
            t += iv[delta]
            if t == number:
                r = a * n + delta + 1
                break
        if t != number:
            raise RuntimeError("iv_decrypt failed: number={}".format(number))
    if flag:
        r = -1 * r
    return r

class EncoderBase(object):

    def encode(self, data):
        raise NotImplementedError()

    def decode(self, data):
        raise NotImplementedError()

class RawDataEncoder(EncoderBase):

    def encode(self, data):
        return data
    
    def decode(self, data):
        return data

class HexlifyEncoder(EncoderBase):

    def encode(self, data):
        if data is None:
            return None
        data = strutils.force_bytes(data)
        return binascii.hexlify(data).decode()

    def decode(self, data):
        if data is None:
            return None
        data = strutils.force_bytes(data)
        return binascii.unhexlify(data)

class Base64Encoder(EncoderBase):

    def encode(self, data):
        if data is None:
            return None
        data = strutils.force_bytes(data)
        return strutils.join_lines(base64.encodebytes(data)).decode()

    def decode(self, data):
        if data is None:
            return None
        data = strutils.force_bytes(data)
        return base64.decodebytes(data)

class SafeBase64Encoder(EncoderBase):

    def encode(self, data):
        if data is None:
            return None
        data = strutils.force_bytes(data)
        return strutils.join_lines(base64.urlsafe_b64encode(data)).decode()

    def decode(self, data):
        if data is None:
            return None
        data = strutils.force_bytes(data)
        return base64.urlsafe_b64decode(data)

class CipherBase(object):

    def get_defaults(self):
        if hasattr(self, "defaults"):
            return getattr(self, "defaults")
        else:
            return {}

    def __init__(self, **kwargs):
        params = {}
        params.update(self.defaults)
        params.update(kwargs)
        self.password = params["password"]
        self._encrypt = params["encrypt"]
        self._decrypt = params["decrypt"]
        self.encrypt_kwargs = params.get("encrypt_kwargs", {})
        self.decrypt_kwargs = params.get("decrypt_kwargs", {})
        self.kwargs = params.get("kwargs", {})
        self.encoder = params["encoder"]
        self.force_text = params.get("force_text", False)
        self.text_encoding = params.get("text_encoding", "utf-8")

    def encrypt(self, data):
        if data is None:
            return None
        params = {}
        params.update(self.kwargs)
        params.update(self.encrypt_kwargs)
        data = strutils.force_bytes(data, self.text_encoding)
        encrypted_data = self._encrypt(data, self.password, **params)
        return self.encoder.encode(encrypted_data)

    def decrypt(self, text):
        if text is None:
            return None
        params = {}
        params.update(self.kwargs)
        params.update(self.decrypt_kwargs)
        data = self.encoder.decode(text)
        decrypted_data = self._decrypt(data, self.password, **params)
        if self.force_text:
            return strutils.force_text(decrypted_data, self.text_encoding)
        else:
            return decrypted_data



class S12Cipher(CipherBase):

    defaults = {
        "encoder": RawDataEncoder(),
        "encrypt": s12_encrypt,
        "decrypt": s12_decrypt,
    }


class AesCipher(CipherBase):
    
    defaults = {
        "encoder": RawDataEncoder(),
        "encrypt": aesutils.encrypt,
        "decrypt": aesutils.decrypt,
    }

class IvCipher(CipherBase):

    defaults = {
        "encoder": RawDataEncoder(),
        "encrypt": iv_encrypt,
        "decrypt": iv_decrypt,
    }
