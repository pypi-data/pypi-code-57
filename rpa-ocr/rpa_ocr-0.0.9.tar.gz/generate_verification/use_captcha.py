# -*- coding:utf-8 -*-
# @author :adolf
from captcha.image import ImageCaptcha
from random import randint
import os
from tqdm import tqdm

english_alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                    'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
                    'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
                    'Z', 'X', 'C', 'V', 'B', 'N', 'M',
                    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
                    'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
                    'z', 'x', 'c', 'v', 'b', 'n', 'm']
# print(len(english_alphabet))
#
for i in tqdm(range(100000)):
    chars = ''
    for i in range(4):
        chars += english_alphabet[randint(0, 61)]
    image = ImageCaptcha().generate_image(chars)

    label_path = 'gen_ver'
    if not os.path.exists(label_path):
        os.mkdir(label_path)
    label = chars + '.png'
    image.save(os.path.join(label_path, label))

# for i in range(199999):
#     print(randint(0, 4))
