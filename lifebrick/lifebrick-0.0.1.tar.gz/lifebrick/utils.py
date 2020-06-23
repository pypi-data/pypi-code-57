"""
#!/usr/bin/env python3
#                            _                _____
#      /\                   | |       /\     |_   _|
#     /  \     ____   __ _  | |_     /  \      | |
#    / /\ \   |_  /  / _` | | __|   / /\ \     | |
#   / ____ \   / /  | (_| | | |_   / ____ \   _| |_
#  /_/    \_\ /___|  \__,_|  \__| /_/    \_\ |_____|
#
#

manily two functions here.
first function, just creates a blank 1000 by 10 000 pixel image.

def gen_10mil():
    pass


second function puts brick image on the canvas image

def put_brick(canvas,img):
    pass

third function removes brick image from the canvas.

def remove_brick(coordinate,canvas):
    pass

"""
import os
import time
from datetime import datetime

import numpy as np
import cv2


def calculator(x1, y1, x2, y2):
    """calculates the human readable brick system to the machine readable cv2 coordinate system"""
    # x1,y1 ------
    # |          |
    # |          |
    # |          |
    # --------x2,y2
    pass


def put_brick(canvas, img):
    """puts brick image on the canvas image"""
    # todo: implement the function


def remove_brick(canvas, coordinate):
    """Removes the given brick coordinate image from the canvas"""
    # todo implement


def brick2pixel(a1, b1, a2, b2):
    """ converts the given brick coordinates to the pixel coordinates, returns such for value"""

    # pixel coordinate
    # x1,y1 ------
    # |          |
    # |          |
    # |          |
    # --------x2,y2

    # brick coordinate
    # ----------------------
    # | (a1,b1) |          |
    # |         | (b1,b2)  |
    # ----------------------

    # a is for row
    # b is for column

    x1 = b1 * 10
    y1 = a1 * 10
    x2 = b2 * 10 + 10
    y2 = a2 * 10 + 10
    return x1, y1, x2, y2


def pixel2brick(x1, y1, x2, y2):
    """converts given pixel coordinates to the brick coordinate"""

    # pixel coordinate
    # x1,y1 ------
    # |          |
    # |          |
    # |          |
    # --------x2,y2

    # brick coordinate
    # ----------------------
    # | (a1,b1) |          |
    # |         | (b1,b2)  |
    # ----------------------

    b1 = x1 // 10
    a1 = y1 // 10
    b2 = (x2 - 10) // 10
    a2 = (y2 - 10) // 10

    return a1, b1, a2, b2


def brick_each(a1, b1, a2, b2):
    """Calculates each brick that selected and returns a list of all envolved bricks"""
    selected = []
    for row in range(a1, a2 + 1):
        for col in range(b1, b2 + 1):
            selected.append((row, col))
    return selected


# brick = brick_each(0, 0, 999, 99)[0]
# roi = brick2pixel(brick[0], brick[1], brick[0], brick[1])
# print(brick)
# print(roi)


def gen_10mil(compress=True):
    """Generates a blank 1000 by 10 000 pixel image."""
    # todo: implement the function
    height = 10000
    width = 1000
    blank_image = np.zeros((height, width, 3), np.uint8)
    blank_image[:, :] = (200, 200, 200)  # (B, G, R)
    # get pixel value for each 10000 brick
    selected_bricks = brick_each(0, 0, 999, 99)
    print(selected_bricks)
    roi = []
    for brick in selected_bricks:
        roi.append(brick2pixel(brick[0], brick[1], brick[0], brick[1]))
    print(roi)

    color = (26, 127, 239)
    thickness = 1

    for each in roi:
        start_point = (each[0], each[1])
        end_point = (each[2], each[3])
        image = cv2.rectangle(blank_image, start_point, end_point, color, thickness)

    # save the img to the disk

    if compress is True:
        print("compressing....")
        cv2.imwrite('pixel.png', image, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
    else:
        cv2.imwrite('pixel.png', image)

