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


class S12CipherCore(object):

    def __init__(self, password):
        self.password = password
        self.s12_encode_map = self.get_s12_encode_map()
        self.s12_encode_bytes = self.get_s12_encode_bytes()
        self.s12_decode_bytes = self.get_s12_decode_bytes()

    def get_s12_encode_map(self):
        v = randomutils.Random(self.password).get_bytes(256)
        values = list(range(256))
        delta = 0
        for index in range(256):
            delta += v[index]
            values[index] += delta
        return values

    def get_s12_encode_bytes(self):
        encode_map = self.s12_encode_map
        encode_bytes = {}
        for code in range(256):
            value = encode_map[code]
            high = value // 256
            low = value % 256
            encode_bytes[bytes([code])] = bytes([high, low])
        return encode_bytes

    def get_s12_decode_bytes(self):
        encode_map = self.s12_encode_map
        decode_bytes = {}
        for code in range(256):
            value = encode_map[code]
            high = value // 256
            low = value % 256
            decode_bytes[bytes([high, low])] = bytes([code])
        return decode_bytes

    def encrypt(self, data, **kwargs):
        data = strutils.force_bytes(data)
        encode_bytes = self.s12_encode_bytes
        return b"".join([encode_bytes[bytes([code])] for code in data])

    def decrypt(self, data, **kwargs):
        result = b''
        decode_bytes = self.s12_decode_bytes
        for start in range(0, len(data), 2):
            result += decode_bytes[data[start: start + 2]]
        return result

def s12_encrypt(data, password):
    cipher = S12CipherCore(password)
    return cipher.encrypt(data)

def s12_decrypt(data, password):
    cipher = S12CipherCore(password)
    return cipher.decrypt(data)



class IvCipherCore(object):
    def __init__(self, password):
        self.password = password
        self.iv_params = self.get_iv_params()

    def get_iv_params(self):
        gen = randomutils.Random(self.password)
        n = gen.randint(9999, 1024)
        iv = [gen.randint(100, 1) for _ in range(n)]
        return n, iv

    def encrypt(self, number, **kwargs):
        number = strutils.force_int(number)
        flag = False
        if number < 0:
            number = -1 * number
            flag = True
        n, iv = self.iv_params
        s = sum(iv)
        a = number // n
        b = number % n
        r = a * s + sum(iv[:b])
        if flag:
            r = -1 * r
        return r

    def decrypt(self, number, **kwargs):
        number = strutils.force_int(number)
        flag = False
        if number < 0:
            number = -1 * number
            flag = True
        n, iv = self.iv_params
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

def iv_encrypt(number, password):
    cipher = IvCipherCore(password)
    return cipher.encrypt(number)

def iv_decrypt(number, password):
    cipher = IvCipherCore(password)
    return cipher.decrypt(number)

class IvfCipherCore(IvCipherCore):

    def __init__(self, password, int_digits=12, float_digits=4):
        super().__init__(password)
        self.int_digits = int_digits
        self.float_digits = float_digits
        self.module = 10 ** ((int_digits + float_digits) * 2)
        self.max_value_length = ((int_digits + float_digits) * 4)
        self.max = 10 ** self.max_value_length - 1
        self.value_template = "{:0%dd}" % self.max_value_length

    def encrypt(self, number, **kwargs):
        number = int(number * self.module)
        number = super().encrypt(number)
        if number >= 0:
            return "+" + self.value_template.format(number)
        else:
            return "*" + self.value_template.format(self.max - abs(number))

    def decrypt(self, number, **kwargs):
        sign = number[0]
        number = int(number[1:])
        if sign == "*":
            number = self.max - number
        number = super().decrypt(number)
        number = round(number / (self.module + 8), self.float_digits)
        if sign == "*":
            return -1 * number
        else:
            return number

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
        self.password = params.get("password", None)
        self.encrypt_kwargs = params.get("encrypt_kwargs", {})
        self.decrypt_kwargs = params.get("decrypt_kwargs", {})
        self.kwargs = params.get("kwargs", {})
        if self.password:
            self.kwargs.update({"password": self.password})
        self.encoder = params["encoder"]
        self.force_text = params.get("force_text", False)
        self.text_encoding = params.get("text_encoding", "utf-8")
        self.cipher_core_class = params.get("cipher_core", None)
        if self.cipher_core_class:
            self.cipher_instance = self.cipher_core_class(**self.kwargs)
            self._encrypt = self.cipher_instance.encrypt
            self._decrypt = self.cipher_instance.decrypt
        else:
            self._encrypt = params["encrypt"]
            self._decrypt = params["decrypt"]

    def encrypt(self, data):
        if data is None:
            return None
        params = {}
        params.update(self.kwargs)
        params.update(self.encrypt_kwargs)
        data = strutils.force_bytes(data, self.text_encoding)
        encrypted_data = self._encrypt(data, **params)
        return self.encoder.encode(encrypted_data)

    def decrypt(self, text):
        if text is None:
            return None
        params = {}
        params.update(self.kwargs)
        params.update(self.decrypt_kwargs)
        data = self.encoder.decode(text)
        decrypted_data = self._decrypt(data, **params)
        if self.force_text:
            return strutils.force_text(decrypted_data, self.text_encoding)
        else:
            return decrypted_data

class AesCipher(CipherBase):
    
    defaults = {
        "encoder": RawDataEncoder(),
        "encrypt": aesutils.encrypt,
        "decrypt": aesutils.decrypt,
    }

class S12Cipher(CipherBase):

    defaults = {
        "encoder": RawDataEncoder(),
        "cipher_core": S12CipherCore,
    }

class IvCipher(CipherBase):

    defaults = {
        "encoder": RawDataEncoder(),
        "cipher_core": IvCipherCore,
    }

class IvfCipher(CipherBase):

    defaults = {
        "encoder": RawDataEncoder(),
        "cipher_core": IvfCipherCore,
        "kwargs": {
            "int_digits": 12,
            "float_digits": 4,
        }
    }
