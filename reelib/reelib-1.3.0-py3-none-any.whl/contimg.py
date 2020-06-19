import random

import cv2
import numpy as np
from PIL import Image


def cv2pil(img):
    """OpenCV->PIL"""
    new_img = img.copy()
    if new_img.ndim == 2:  # モノクロ
        pass
    elif new_img.shape[2] == 3:  # カラー
        new_img = new_img[:, :, ::-1]
    elif new_img.shape[2] == 4:  # 透過
        new_img = new_img[:, :, [2, 1, 0, 3]]
    new_img = Image.fromarray(new_img)
    return new_img


def pil2cv(img):
    """PIL->OpenCV"""
    new_img = np.array(img, dtype=np.uint8)
    if new_img.ndim == 2:  # モノクロ
        pass
    elif new_img.shape[2] == 3:  # カラー
        new_img = new_img[:, :, ::-1]
    elif new_img.shape[2] == 4:  # 透過
        new_img = new_img[:, :, [2, 1, 0, 3]]
    return new_img


def resize(frame, output_size, fill=True):
    """画像のリサイズ"""
    x = frame.shape[1]
    y = frame.shape[0]
    out_x, out_y = output_size
    f_rate = x / y
    o_rate = out_x / out_y
    if fill:
        if f_rate == o_rate:
            frame_r = np.copy(frame)
        elif f_rate >= o_rate:
            y_r = x // o_rate
            start = (y_r - y) // 2
            fin = (y_r + y) // 2
            frame_r = cv2.resize(np.zeros((1, 1, 3), np.uint8), (x, y_r))
            frame_r[start:fin, :] = frame
        else:
            x_r = int(y * o_rate)
            start = (x_r - x) // 2
            fin = (x_r + x) // 2
            frame_r = cv2.resize(np.zeros((1, 1, 3), np.uint8), (x_r, y))
            frame_r[:, start:fin] = frame
    else:
        if f_rate == o_rate:
            frame_r = np.copy(frame)
        elif f_rate >= o_rate:
            x_r = int(y * o_rate)
            d = x - x_r
            s_x = d // 2
            frame_r = frame[:, s_x : s_x + y]
        else:
            y_r = x // o_rate
            d = y - y_r
            s_y = d // 2
            frame_r = frame[s_y : s_y + x, :]
    frame_r = cv2.resize(frame_r, dsize=output_size)
    return frame_r


def get_imagetile(img_path_list, img_size, img_num, fill=True):
    """画像タイルの作成"""
    size_x, size_y = img_size
    num_x, num_y = img_num

    if len(img_path_list) >= num_x * num_y:
        imgs = sorted(random.sample(img_path_list, num_x * num_y))
    else:
        imgs = sorted(img_path_list)

    frame = np.zeros((size_y * num_y, size_x * num_x, 3), np.uint8)

    for i, img in enumerate(imgs):
        f = cv2.imread(img)
        f = resize(f, img_size, fill=fill)
        x = i % num_x
        y = i // num_y
        frame[size_y * y : size_y * (y + 1), size_x * x : size_x * (x + 1)] = f

    return frame
