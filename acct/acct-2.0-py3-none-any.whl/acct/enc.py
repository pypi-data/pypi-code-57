# Import python libs
import os

# Import third party libs
from cryptography.fernet import Fernet
import yaml
import msgpack


def encrypt(hub, fn, key=None):
    ret = {}
    print_key = False
    if key is None:
        print_key = True
        key = Fernet.generate_key()
    f = Fernet(key)
    tfn = f"{fn}.fernet"
    with open(fn, "rb") as rfh:
        data = yaml.safe_load(rfh.read())
    with open(tfn, "wb+") as wfh:
        wfh.write(f.encrypt(msgpack.dumps(data)))
    ret["msg"] = f"New encrypted file created at: {tfn}\n"
    if isinstance(key, bytes):
        key = key.decode()
    if print_key:
        ret["msg"] += f"The file was encrypted with this key:\n{key}"
    return ret


def file_decrypt(hub, fn, key):
    """
    Given the file and key, save a relative file that is decrypted
    """
    data = yaml.dump(hub.acct.init.data_decrypt(fn, key))
    if fn.endswith(".fernet"):
        sfn = fn.rstrip(".fernet")
    else:
        sfn = f"{fn}.clear"
    with open(sfn, "wb+") as wfh:
        wfh.write(data)


def data_decrypt(hub, fn, key):
    """
    Decrypt the given file with the given key
    """
    if not os.path.isfile(fn):
        raise FileNotFoundError(f"Account file {fn} not found")
    f = Fernet(key)
    with open(fn, "rb") as rfh:
        raw = f.decrypt(rfh.read())
    return msgpack.loads(raw)
