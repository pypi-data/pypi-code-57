import random
import hmac
import base64
from hashlib import sha256


def random_password(length):
    base_char = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'I', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'i', 'h', 'j', 'k', 'l',
                 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4',
                 '5', '6', '7', '8', '9', '!', '@', '#', '$', '%', '^', '&', '*']
    password = ''
    for j in range(length):
        m = random.randint(0, len(base_char) - 1)
        password = password + base_char[m]
    return password


def rc4_init_s_box(key):
    s_box = list(range(256))
    j = 0
    for i in range(256):
        j_step_1 = j + s_box[i]
        j_step_2 = j_step_1 + ord(key[i % len(key)])
        j_step_3 = j_step_2 % 256
        j = j_step_3
        s_box[i], s_box[j] = s_box[j], s_box[i]
    return s_box


def rc4_res_program(s_box, message):
    res = []
    i = j = 0
    for s in message:
        i = (i + 1) % 256
        j = (j + s_box[i]) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]
        t = (s_box[i] + s_box[j]) % 256
        k = s_box[t]
        res.append(chr(ord(s) ^ k))
    return res


def encryption_rc4(key, message):
    s_box = rc4_init_s_box(key)
    res = rc4_res_program(s_box, message)
    cipher = "".join(res)
    cipher_text = str(base64.b64encode(cipher.encode('utf-8')), 'utf-8')
    return cipher_text


def decrypt_rc4(key, message):
    s_box = rc4_init_s_box(key)
    plain = base64.b64decode(message.encode('utf-8'))
    plain = bytes.decode(plain)
    res = rc4_res_program(s_box, plain)
    cipher = "".join(res)
    return cipher


def hmac_sha256_digest(value, key='35a07615d258ae2e067879a472e050cc3716'):
    app_secret = key.encode('utf-8')
    data = value.encode('utf-8')
    signature = base64.b64encode(hmac.new(app_secret, data, digestmod=sha256).digest())
    return signature
