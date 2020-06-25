# -*- coding: utf-8 -*-
import functools
import random
import string
import os
import binascii
import base64
import bizerror
import typing
from decimal import Decimal

try:
    text_type = unicode
    bytes_type = str
except NameError:
    text_type = str
    bytes_type = bytes

HEXLIFY_CHARS = "0123456789abcdefABCDEF"
URLSAFEB64_CHARS = "-0123456789=ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz\r\n"
BASE64_CHARS = "+/0123456789=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\r\n"

default_encodings = ["utf8", "gb18030"]


def random_string(length, choices=string.ascii_letters):
    text = ""
    for _ in range(0, length):
        text += random.choice(choices)
    return text

def char_force_to_int(value):
    if isinstance(value, int):
        return value
    return ord(value)

def force_bytes(value, encoding="utf-8"):
    if isinstance(value, text_type):
        encoding = encoding or "utf-8"
        return value.encode(encoding)
    else:
        return value

def force_text(value, encoding=None):
    if isinstance(value, text_type):
        return value
    if not encoding:
        encodings = default_encodings
    elif isinstance(encoding, (set, list, tuple)):
        encodings = encoding
    else:
        encodings = [encoding]
    for encoding in encodings:
        try:
            return value.decode(encoding)
        except UnicodeDecodeError:
            pass
    raise UnicodeDecodeError()

def force_int(value):
    if isinstance(value, int):
        return value
    elif isinstance(value, str):
        return int(value)
    elif isinstance(value, bytes):
        return int(value.decode())
    elif isinstance(value, float):
        return int(value)
    elif isinstance(value, Decimal):
        return int(value)
    else:
        raise RuntimeError("force_int failed: value={}".format(value))

def wholestrip(text):
    """Remove all white spaces in text. White spaces are ' \t\n\r\x0b\x0c\u3000'.
    """
    for space in string.whitespace + u'\u3000':
        text = text.replace(space, "")
    return text


def split(text, seps, strip=False):
    """seps is a list of string, all sep in the seps are treated as delimiter.
    """
    if not isinstance(seps, (list, set, tuple)):
        seps = [seps]
    results = [text]
    for sep in seps:
        row = []
        for value in results:
            row += value.split(sep)
        results = row
    if strip:
        row = []
        for value in results:
            row.append(value.strip())
        results = row
    return results


def str_composed_by(text, choices):
    """Test if text is composed by chars in the choices.
    """
    for char in text:
        if not char in choices:
            return False
    return True

is_str_composed_by_the_choices = str_composed_by


def is_hex_digits(text):
    """Test if all chars in text is hex digits.
    """
    if not text:
        return False
    return str_composed_by(text, HEXLIFY_CHARS)

def join_lines(text):
    """Join multi-lines into single line.
    """
    if isinstance(text, str):
        return "".join(text.splitlines())
    elif isinstance(text, bytes):
        return b"".join(text.splitlines())


def is_urlsafeb64_decodable(text):
    """Test if the text can be decoded by urlsafeb64 method.
    """
    text = wholestrip(text)
    if not text:
        return False
    if len(text) % 4 != 0:
        return False
    return str_composed_by(join_lines(text), URLSAFEB64_CHARS)


def is_base64_decodable(text):
    """Test  if the text can be decoded by base64 method.
    """
    text = wholestrip(text)
    if not text:
        return False
    if len(text) % 4 != 0:
        return False
    return str_composed_by(join_lines(text), BASE64_CHARS)


def is_unhexlifiable(text):
    """Test if the text can be decoded by unhexlify method.
    """
    text = wholestrip(text)
    if not text:
        return False
    if len(text) % 2 != 0:
        return False
    return str_composed_by(text, HEXLIFY_CHARS)


def text_display_length(text, unicode_display_length=2, encoding=None):
    """Get text display length.
    """
    text = force_text(text, encoding)
    length = 0
    for c in text:
        if ord(c) <= 128:
            length += 1
        else:
            length += unicode_display_length
    return length

def text_display_shorten(text, max_length, unicode_display_length=2, suffix="...", encoding=None):
    """Shorten text to fix the max display length.
    """
    text = force_text(text, encoding)
    if max_length < len(suffix):
        max_length = len(suffix)
    tlen = text_display_length(text, unicode_display_length=unicode_display_length)
    if tlen <= max_length:
        return text
    result = ""
    tlen = 0
    max_length -= len(suffix)
    for c in text:
        if ord(c) <= 128:
            tlen += 1
        else:
            tlen += unicode_display_length
        if tlen < max_length:
            result += c
        elif tlen == max_length:
            result += c
            break
        else:
            break
    result += suffix
    return result

def smart_get_binary_data(text: typing.Union[str, bytes]) -> bytes:
    if isinstance(text, str):
        if is_unhexlifiable(text):
            return binascii.unhexlify(text)
        elif is_urlsafeb64_decodable(text):
            return base64.urlsafe_b64decode(text.encode("utf-8"))
        elif is_base64_decodable(text):
            return base64.decodebytes(text.encode("utf-8"))
        else:
            return text.encode("utf-8")
    elif isinstance(text, bytes):
        return text
    else:
        raise bizerror.NotSupportedTypeToCast()

def is_chinese_character(c: str) -> bool:
    """
    Block                                   Range       Comment
    CJK Unified Ideographs                  4E00-9FFF   Common
    CJK Unified Ideographs Extension A      3400-4DBF   Rare
    CJK Unified Ideographs Extension B      20000-2A6DF Rare, historic
    CJK Unified Ideographs Extension C      2A700–2B73F Rare, historic
    CJK Unified Ideographs Extension D      2B740–2B81F Uncommon, some in current use
    CJK Unified Ideographs Extension E      2B820–2CEAF Rare, historic
    CJK Compatibility Ideographs            F900-FAFF   Duplicates, unifiable variants, corporate characters
    CJK Compatibility Ideographs Supplement 2F800-2FA1F Unifiable variants
    """
    c = ord(c)
    if 0x4E00 <= c <= 0x9FFF:
        return True
    if 0x3400 <= c <= 0x4DBF:
        return True
    if 0x20000 <= c <= 0x2A6DF:
        return True
    if 0x2A700 <= c <= 0x2B73F:
        return True
    if 0x2B740 <= c <= 0x2B81F:
        return True
    if 0x2B820 <= c <= 0x2CEAF:
        return True
    if 0xF900 <= c <= 0xFAFF:
        return True
    if 0x2F800 <=c <= 0x2FA1F:
        return True
    return False

def binarify(data: typing.Union[str, bytes]) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return "".join(["{:08b}".format(x) for x in data])

def unbinarify(text: typing.Union[str, bytes]) -> bytes:
    if not text:
        return b""
    if isinstance(text, bytes):
        text = text.decode("utf-8")
    from .listutils import chunk
    return bytes([int(x, 2) for x in chunk(text, 8)])

def ints2bytes(ints: typing.List[int]) -> bytes:
    result = b""
    for value in ints:
        if value:
            result += int2bytes(value)
        else:
            result += b'\x00'
    return result

def int2bytes(value: int):
    bs = []
    while value:
        bs.append(value % 256)
        value = value // 256
    bs.reverse()
    return bytes(bs)
