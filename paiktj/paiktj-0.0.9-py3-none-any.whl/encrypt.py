import pickle
from getpass import getpass
from cryptography.fernet import Fernet


def my_encrypt(object_input, key_save=False, file_name=None):
    """
    :param object_input:
    :param key_save:
    :param file_name:
    :return:
    """
    if key_save and file_name is None:
        raise Exception("file name needed")
    while True:
        dialog = input("file is small (y or n)")
        if dialog == "n":
            return
        elif dialog == "y":
            break
        else:
            print("wrong answer")
    string_object = pickle.dumps(object_input)
    key = Fernet.generate_key()
    if key_save:
        with open(file_name, 'wb') as f:
            f.write(key)
    else:
        print("'''", end="")
        print(key)
        print("'''", end="")
    f = Fernet(key)
    return f.encrypt(string_object)


def my_decrypt(string_encrypted):
    """
    :param string_encrypted:
    :return:
    """
    key = getpass("key : ")
    f = Fernet(key)
    string_decrypted = f.decrypt(string_encrypted)
    return pickle.loads(string_decrypted)


def my_encrypt_save(object_input, key_save, key_file_name, data_file_name):
    """
    :param object_input:
    :param key_save:
    :param key_file_name:
    :param data_file_name:
    :return:
    """
    encrypted = my_encrypt(object_input, key_save, key_file_name)
    with open(data_file_name, 'wb') as f:
        f.write(encrypted)


def my_decrypt_load(file_name):
    """
    :param file_name:
    :return:
    """
    with open(file_name, 'rb') as f:
        string_encrypted = f.read()
    key = getpass("key : ")
    f = Fernet(key)
    return my_decrypt(f.decrypt(string_encrypted))


# def my_encrypt_file2file(object_path, save_path="./"):
#     file_name = object_path.split("/")[-1]
#     with open(object_path, 'rb') as f:
#         contents = f.read()
#     key = Fernet.generate_key()
#     f = Fernet(key)
#     print("encrypting...", end='')
#     encrypted = f.encrypt(contents)
#     print("done")
#     with open(save_path + "/" + file_name + ".data", 'wb') as f:
#         f.write(encrypted)
#     with open(save_path + "/" + file_name + ".key", 'wb') as f:
#         f.write(key)
#
#
# def my_decrypt_file2mem(object_path):
#     with open(object_path, 'rb') as f:
#         string_encrypted = f.read()
#     key = getpass("key : ")
#     f = Fernet(key)
#     print("encrypting...", end='')
#     result = f.decrypt(string_encrypted)
#     print("done")
#     return result
#

def my_encrypt_mem2mem(object_input):
    string_object = pickle.dumps(object_input)
    key = Fernet.generate_key()
    f = Fernet(key)
    print("encrypting...", end='')
    encrypted = f.encrypt(string_object)
    print("done")
    return encrypted, key


def my_encrypt_file2file(func, object_path, save_folder_path, **kwargs):
    file_name = object_path.split("/")[-1]
    tmp_object = func(object_path, **kwargs)
    encrypted, key = my_encrypt_mem2mem(tmp_object)
    with open(save_folder_path + "/" + file_name + ".data", 'wb') as f:
        f.write(encrypted)
    with open(save_folder_path + "/" + file_name + ".key", 'wb') as f:
        f.write(key)


def my_decrypt_mem2mem(object_input):
    key = getpass("key : ")
    f = Fernet(key)
    decrypted = f.decrypt(object_input)
    return pickle.loads(decrypted)


def my_decrypt_file2mem(object_path):
    with open(object_path, 'rb') as f:
        encrypted = f.read()
    return my_decrypt_mem2mem(encrypted)
