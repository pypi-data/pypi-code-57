from cryptography.fernet import Fernet


def byte():
    return " ".encode()


def generate_key():
    key = Fernet.generate_key()
    return key


def save_and_create_key():
    key = Fernet.generate_key()
    file = open('key.key', 'wb')
    file.write(key)
    file.close()


def get_key():
    try:
        file = open('key.key', 'rb')
        key = file.read()
        file.close()
        return key
    except:
        raise FileNotFoundError("Key file no found. NOTE:- make sure you have excuted save_and_crate_key() before this")


# noinspection PyBroadException,PyUnboundLocalVariable
def encrypt(message_to_encrypt, key):
    try:
        message = message_to_encrypt.encode()
    except:
        message = message_to_encrypt
    finally:
        f = Fernet(key)
        encrypted = f.encrypt(message)
        return encrypted


def decrypt(message_to_decrypt, key):
    try:
        message_to_decrypt = message_to_decrypt.encode()
    finally:
        message = message_to_decrypt
        f = Fernet(key)
        decrypted = f.decrypt(message)
        decrypted = decrypted.decode()
        return decrypted
