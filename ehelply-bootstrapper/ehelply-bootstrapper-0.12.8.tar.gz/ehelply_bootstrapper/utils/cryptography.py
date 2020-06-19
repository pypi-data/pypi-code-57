from cryptography.fernet import Fernet, MultiFernet
import math
import time
import bcrypt
from typing import List, Tuple
import json


class Encryption:
    """
    Provides a small wrapper over the cryptography fernet library
    """

    STRING_ENCODING: str = "utf-8"

    def __init__(self, keys: List[bytes]) -> None:
        """
        Takes in byte keys, translates them to Fernet keys, and creates a MultiFernet instance
        :param keys:
        """
        self.keys: List[Fernet] = []

        for key in keys:
            self.keys.append(Fernet(key))

        self.multi_fernet: MultiFernet = MultiFernet(self.keys)

    @staticmethod
    def generate_key():
        return Fernet.generate_key()

    def add_key(self, key: bytes):
        """
        Adds a new key to our MultiFernet instance. This key will become the encryption key
        :param key:
        :return:
        """
        self.multi_fernet = MultiFernet([Fernet(key)] + self.keys)

    def remove_key(self, key: bytes):
        """
        Removes all instances of a key. Decryptions with this key will no longer be valid
        :param key:
        :return:
        """
        target: Fernet = Fernet(key)
        for key in self.keys:
            if target._signing_key == key._signing_key and target._encryption_key == key._encryption_key:
                self.keys.remove(key)

    def rotate(self, data: bytes) -> bytes:
        """
        Rotate data encrypted using an old key to the latest key
        :param data:
        :return:
        """
        return self.multi_fernet.rotate(data)

    def encrypt(self, data) -> bytes:
        """
        Encrypts any data that can be casted to bytes
        :param data:
        :return:
        """
        if isinstance(data, list) or isinstance(data, dict):
            data: str = json.dumps(data)
        data: bytes = str(data).encode(Encryption.STRING_ENCODING)
        return self.multi_fernet.encrypt(data)

    def decrypt(self, data: bytes, ttl_seconds: int = None) -> bytes:
        """
        Decrypts data and returns bytes.
        :param data:
        :param ttl_seconds: The amount of seconds old the data can be to be valid. Leave as None for inf
        :return:
        """
        return self.multi_fernet.decrypt(data, ttl=ttl_seconds)

    def decrypt_str(self, data, ttl_seconds: int = None) -> str:
        """
        Decrypts a string
        :param data:
        :param ttl_seconds: The amount of seconds old the data can be to be valid. Leave as None for inf
        :return:
        """
        return str(self.decrypt(data, ttl_seconds).decode(Encryption.STRING_ENCODING))

    def decrypt_int(self, data, ttl_seconds: int = None) -> int:
        """
        Decrypts an int
        :param data:
        :param ttl_seconds: The amount of seconds old the data can be to be valid. Leave as None for inf
        :return:
        """
        return int(self.decrypt_str(data, ttl_seconds))

    def decrypt_float(self, data, ttl_seconds: int = None) -> float:
        """
        Decrypts a float
        :param data:
        :param ttl_seconds: The amount of seconds old the data can be to be valid. Leave as None for inf
        :return:
        """
        return float(self.decrypt_str(data, ttl_seconds))

    def decrypt_list(self, data, ttl_seconds: int = None) -> list:
        """
        Decrypts a list
        :param data:
        :param ttl_seconds: The amount of seconds old the data can be to be valid. Leave as None for inf
        :return:
        """
        return list(json.loads(self.decrypt_str(data, ttl_seconds)))

    def decrypt_dict(self, data, ttl_seconds: int = None) -> dict:
        """
        Decrypts a dict
        :param data:
        :param ttl_seconds: The amount of seconds old the data can be to be valid. Leave as None for inf
        :return:
        """
        return dict(json.loads(self.decrypt_str(data, ttl_seconds)))


class Hashing:
    COST_FACTOR: int = 10

    def hash_timed(self, data) -> Tuple[str, float]:
        start = time.time()
        myhash = self.hash(data)
        end = time.time()
        return myhash, end - start

    def hash(self, data) -> str:
        salt = bcrypt.gensalt(rounds=Hashing.COST_FACTOR)
        if isinstance(data, str):
            data = data.encode(Encryption.STRING_ENCODING)
        return bcrypt.hashpw(data, salt)

    def check(self, data, myhash) -> bool:
        if isinstance(data, str):
            data = data.encode(Encryption.STRING_ENCODING)
        if isinstance(myhash, str):
            myhash = myhash.encode(Encryption.STRING_ENCODING)
        return bcrypt.checkpw(data, myhash)
