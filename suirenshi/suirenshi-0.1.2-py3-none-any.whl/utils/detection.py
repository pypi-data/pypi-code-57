# -*- coding: UTF-8 -*-
################################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
本文件定义了检测模型常用工具。

Authors: liuyawen03(liuyawen03@baidu.com)
Date:    2020/06/11 22:00:29
"""

import cv2
from skimage.filters import unsharp_mask
import numpy as np


def compute_iou(bbox1, bbox2):
    """
    Args:
        bbox1, bbox2: 待计算的2个框
    Returns: iou
    """
    bbox1xmin = bbox1[0]
    bbox1ymin = bbox1[1]
    bbox1xmax = bbox1[2]
    bbox1ymax = bbox1[3]
    bbox2xmin = bbox2[0]
    bbox2ymin = bbox2[1]
    bbox2xmax = bbox2[2]
    bbox2ymax = bbox2[3]
    area1 = (bbox1ymax - bbox1ymin) * (bbox1xmax - bbox1xmin)
    area2 = (bbox2ymax - bbox2ymin) * (bbox2xmax - bbox2xmin)
    bboxxmin = max(bbox1xmin, bbox2xmin)
    bboxxmax = min(bbox1xmax, bbox2xmax)
    bboxymin = max(bbox1ymin, bbox2ymin)
    bboxymax = min(bbox1ymax, bbox2ymax)
    if bboxxmin >= bboxxmax:
        return 0
    if bboxymin >= bboxymax:
        return 0
    area = (bboxymax - bboxymin) * (bboxxmax - bboxxmin)
    iou = area / (area1 + area2 - area)
    return iou


def nms(dets):
    """
    极大值抑制函数
    Args:
        dets: 所有检出框
    Returns: filtered_dets 过滤后的检测框
    """


# 包括传统cv算法等，如unsharp
def unsharp(img_np, radius=5, amount=2):
    """unsharp"""
    # img_np_gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    img_np_gb = cv2.GaussianBlur(img_np, (3, 3), 0)
    img_np_um = unsharp_mask(img_np_gb, radius=radius, amount=amount) * 255
    return img_np_um.astype(np.uint8)


def downsample(img_np, ratio):
    """downsample"""
    height, width = img_np.shape[0], img_np.shape[1]
    img_np_ds = cv2.resize(img_np,
                           (int(width * ratio), int(height * ratio)),
                           interpolation=cv2.INTER_AREA)
    return img_np_ds


def ds_um_enhance(img_np, radius=5, amount=2, ds_ratio=0.0625):
    """downsample_dir"""
    img_np_ds = downsample(img_np, ratio=ds_ratio)
    img_np_ds_um = unsharp(img_np_ds, radius=radius, amount=amount)

    return img_np_ds_um