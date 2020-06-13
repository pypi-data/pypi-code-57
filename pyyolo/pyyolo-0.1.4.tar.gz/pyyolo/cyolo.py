#!/usr/bin/env python3

from ctypes import *

import numpy as np

import os
import sys

try:
    shared_library = None
    shared_library = os.environ['LIB_DARKNET']
    if not os.path.exists(shared_library):
            raise ValueError(f'Path "{shared_library}" does not exist.')
    else:
        import fnmatch
        if not fnmatch.fnmatch(shared_library, '*.so'):
            raise ValueError(f'{shared_library} is not a shared_library')
except KeyError as exception:
    sys.exit('LIB_DARKNET variable is not set.')
except ValueError as exception:
    sys.exit(exception)

class BOX(Structure):
    _fields_ = [('x', c_float),
                ('y', c_float),
                ('w', c_float),
                ('h', c_float)]


class DETECTION(Structure):
    _fields_ = [('bbox', BOX),
                ('classes', c_int),
                ('prob', POINTER(c_float)),
                ('mask', POINTER(c_float)),
                ('objectness', c_float),
                ('sort_class', c_int)]


class IMAGE(Structure):
    _fields_ = [('w', c_int),
                ('h', c_int),
                ('c', c_int),
                ('data', POINTER(c_float))]


class METADATA(Structure):
    _fields_ = [('classes', c_int),
                ('names', POINTER(c_char_p))]

lib = CDLL(shared_library, RTLD_GLOBAL)
lib.network_width.argtypes = [c_void_p]
lib.network_width.restype = c_int
lib.network_height.argtypes = [c_void_p]
lib.network_height.restype = c_int

predict = lib.network_predict
predict.argtypes = [c_void_p, POINTER(c_float)]
predict.restype = POINTER(c_float)

set_gpu = lib.cuda_set_device
set_gpu.argtypes = [c_int]

make_image = lib.make_image
make_image.argtypes = [c_int, c_int, c_int]
make_image.restype = IMAGE

get_network_boxes = lib.get_network_boxes
get_network_boxes.argtypes = \
    [c_void_p, c_int, c_int, c_float, c_float, POINTER(
      c_int), c_int, POINTER(c_int), c_int]
get_network_boxes.restype = POINTER(DETECTION)

make_network_boxes = lib.make_network_boxes
make_network_boxes.argtypes = [c_void_p]
make_network_boxes.restype = POINTER(DETECTION)

free_detections = lib.free_detections
free_detections.argtypes = [POINTER(DETECTION), c_int]

free_ptrs = lib.free_ptrs
free_ptrs.argtypes = [POINTER(c_void_p), c_int]

network_predict = lib.network_predict
network_predict.argtypes = [c_void_p, POINTER(c_float)]

reset_rnn = lib.reset_rnn
reset_rnn.argtypes = [c_void_p]

load_net = lib.load_network
load_net.argtypes = [c_char_p, c_char_p, c_int]
load_net.restype = c_void_p

load_net_custom = lib.load_network_custom
load_net_custom.argtypes = [c_char_p, c_char_p, c_int, c_int]
load_net_custom.restype = c_void_p

do_nms_obj = lib.do_nms_obj
do_nms_obj.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

do_nms_sort = lib.do_nms_sort
do_nms_sort.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

free_image = lib.free_image
free_image.argtypes = [IMAGE]

letterbox_image = lib.letterbox_image
letterbox_image.argtypes = [IMAGE, c_int, c_int]
letterbox_image.restype = IMAGE

load_meta = lib.get_metadata
lib.get_metadata.argtypes = [c_char_p]
lib.get_metadata.restype = METADATA

load_image = lib.load_image_color
load_image.argtypes = [c_char_p, c_int, c_int]
load_image.restype = IMAGE

rgbgr_image = lib.rgbgr_image
rgbgr_image.argtypes = [IMAGE]

predict_image = lib.network_predict_image
predict_image.argtypes = [c_void_p, IMAGE]
predict_image.restype = POINTER(c_float)

def array_to_image(arr):
    arr = arr.transpose(2, 0, 1)
    c = arr.shape[0]
    h = arr.shape[1]
    w = arr.shape[2]
    arr = np.ascontiguousarray(arr.flat, dtype=np.float32) / 255.0
    data = arr.ctypes.data_as(POINTER(c_float))
    im = IMAGE(w, h, c, data)
    return im, arr
