"""Utilities for incached"""
import hashlib
import pickle
import copy
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from .exceptions import IncorrentPasswordException


def load_full_cache(path: str, encrypt: bool = True, password: str = "incached_password"):
    """Load full-dumped cache from file"""
    if encrypt:
        init_vector = b""
        data = b""
        password_hash = hashlib.sha256()
        password_hash.update(password.encode())
        with open(path, "rb") as inp:
            init_vector = inp.read(16)
            data = inp.read()
        cipher = AES.new(password_hash.digest(), AES.MODE_CBC, init_vector)
        try:
            dec_data = unpad(cipher.decrypt(data), AES.block_size)
        except ValueError:
            raise IncorrentPasswordException
        del data
        return pickle.loads(dec_data)
    with open(path, "rb") as inp:
        return pickle.load(inp)


def save_full_cache(path: str, cache_obj, encrypt: bool = True, password: str = "incached_password"):
    """Full dump cache to file"""
    if encrypt:
        password_hash = hashlib.sha256()
        password_hash.update(password.encode())
        cipher = AES.new(password_hash.digest(), AES.MODE_CBC)
        tosave_cache = copy.deepcopy(cache_obj)
        tosave_cache.original = False  # for future versions
        data = pickle.dumps(tosave_cache, pickle.HIGHEST_PROTOCOL)
        enc_bytes = cipher.encrypt(pad(data, AES.block_size))
        with open(path, "wb") as output:
            output.write(cipher.iv)
            output.write(enc_bytes)
        del tosave_cache
        del cipher
        del data
        del enc_bytes
    else:
        with open(path, "wb") as output:
            tosave_cache = copy.deepcopy(cache_obj)
            tosave_cache.original = False  # for future versions
            pickle.dump(tosave_cache, output, pickle.HIGHEST_PROTOCOL)
        del tosave_cache
