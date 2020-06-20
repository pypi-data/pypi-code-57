from cryptography.fernet import Fernet


def generate_key():
    key = Fernet.generate_key()
    return key


def save_and_create_key():
    key = Fernet.generate_key()
    file = open('key.key', 'wb')
    file.write(key)
    file.close()


def get_key():
    file = open('key.key', 'rb')
    key = file.read()
    file.close()
    return key


def encrypt(message_to_encrypt, key):
    message = message_to_encrypt.encode()
    f = Fernet(key)
    encrypted = f.encrypt(message)
    return encrypted


def decrypt(message_to_decrypt, key):
    message = message_to_decrypt
    f = Fernet(key)
    decrypted = f.decrypt(message)
    decrypted = decrypted.decode()
    return decrypted
