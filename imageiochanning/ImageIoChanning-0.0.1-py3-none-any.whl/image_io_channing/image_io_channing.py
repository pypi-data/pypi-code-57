# coding=gbk
"""
author(作者): Channing Xie(谢琛)
time(时间): 2020/6/18 6:49
filename(文件名): image_io_channing.py
function description(功能描述):
...
"""
import numpy as np
import cv2


def read_image(path: str, image_type=1):
    """
    读取一张numpy图像。
    :param path: 图像路径
    :param image_type: 1代表rgb、0代表gray、-1代表rgbd？
    :return:
    """
    assert image_type in [-1, 0, 1]
    image = cv2.imdecode(np.fromfile(path, dtype=np.uint8), image_type)
    return image


def save_image(path: str, image: np.ndarray, image_type='.bmp'):
    """
    写入一张numpy图像
    :param path: 存储路径
    :param image: 需要被存储的图像。
    :param image_type: 存储的图像类型，如png、jpg等
    :return:
    """
    assert image_type in ['.bmp', '.png', '.jpg', '.jpeg']
    cv2.imencode(image_type, image)[1].tofile(path)

