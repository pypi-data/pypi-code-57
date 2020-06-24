#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from skimage.color import rgba2rgb


def rgba_2_rgb(img_array):
    num_channel = img_array.shape[2]
    if num_channel == 3:
        return img_array
    rgb_img = rgba2rgb(img_array) * 255.
    return np.asarray(rgb_img.round(), dtype=np.uint8)

