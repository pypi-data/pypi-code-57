#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
"""
# This module provide
# Authors: jiaohanzhe(jiaohanzhe@baidu.com)
# Date: 2020/6/17 4:08 下午
"""
import math


def crop_image(image, crop_width, crop_height, overlap):
    """

    :param image:
    :param crop_width:
    :param crop_height:
    :param overlap:
    :return:
    """
    height, width = image.shape[0], image.shape[1]
    height_len = math.floor(height - overlap) // (crop_height - overlap)
    width_len = math.floor(width - overlap) // (crop_width - overlap)
    start_x, start_y = 0, 0
    sub_images = {}

    for y_index in range(height_len):
        end_y = min(start_y + crop_height, height)
        if end_y - start_y < crop_height:
            start_y = end_y - crop_height
        for x_index in range(width_len):
            end_x = min(start_x + crop_width, width)
            if end_x - start_x < crop_width:
                start_x = end_x - crop_width
            sub_img = image[start_y: end_y + 1, start_x: end_x + 1]
            sub_images[(start_x, start_y)] = sub_img
            start_x = start_x + crop_width - overlap
        start_x = 0
        start_y = start_y + crop_height - overlap
    return sub_images
