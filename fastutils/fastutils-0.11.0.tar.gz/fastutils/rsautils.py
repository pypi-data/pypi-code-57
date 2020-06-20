import rsa
import base64
from rsa import PrivateKey
from rsa import PublicKey
from .strutils import smart_get_binary_data


def newkeys(nbits=2048):
    return rsa.newkeys(nbits)

def load_private_key(text):
    return PrivateKey.load_pkcs1(text.encode("utf-8"))

def load_public_key_from_private_key(text):
    private_key = load_private_key(text)
    return PublicKey(private_key.n, private_key.e)

def encrypt(data: bytes, pk: PublicKey):
    if isinstance(data, str):
        data = data.encode("utf-8")
    encrypted_data = rsa.encrypt(data, pk)
    return "".join(base64.encodebytes(encrypted_data).decode().splitlines())

def decrypt(data: str, sk: PrivateKey):
    encrypted_data = smart_get_binary_data(data)
    data = rsa.decrypt(encrypted_data, sk)
    return data
