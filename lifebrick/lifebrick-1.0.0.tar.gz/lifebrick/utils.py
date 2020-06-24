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

"""
import os
import glob

import numpy as np
import matplotlib.pyplot as plt
import cv2
import lifebrick
import geoip2.database


def brick2pixel(a1, b1, a2, b2):
    """ converts the given brick coordinates to the pixel coordinates, returns such for value"""

    x1 = b1 * 10
    y1 = a1 * 10
    x2 = b2 * 10 + 10
    y2 = a2 * 10 + 10
    return x1, y1, x2, y2


def pixel2brick(x1, y1, x2, y2):
    """converts given pixel coordinates to the brick coordinate"""

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


def gen_10mil():
    """
    Generates a basic 10 million pixel black image and returns an opencv-python image object. this object can be
    saved using cv2.imwrite method. (should use cv2.imwrite('pixel.png', image, [int(cv2.IMWRITE_PNG_COMPRESSION),
    9]) for compression)
    :param:
    :return: cv2.image object
    """
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
    # if compress is True:
    #     print("compressing....")
    #     cv2.imwrite('pixel.png', image, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
    # else:
    #     cv2.imwrite('pixel.png', image)
    # return the cv2 image object
    return image


def get_ip_address(request):
    """
    Get client ip address from the django request.
    :param request:
    :return: client_ip
    """
    ip = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if not ip:
        ip = request.META.get('REMOTE_ADDR', "")
    client_ip = ip.split(",")[-1].split() if ip else ""
    return client_ip


def get_country_info(ip_address):
    """
    Get client country using the given ip address.
    :param ip_address:
    :return: country name,iso_code
    """
    # get the city database object
    mmdb = os.path.join(lifebrick.__path__[0], 'data', 'GeoLite2-City.mmdb')
    reader = geoip2.database.Reader(mmdb)
    response = reader.city(ip_address)
    country_name = response.country.name
    country_iso_code = response.country.iso_code
    return country_name, country_iso_code


def draw_visitors(visitor_data={}):
    """
    Draws the visitor data for passed 8 months. should used with schedule and update the data each day.
    :param visitor_data: python dictionary. { '2020-03': 1324, '2020-04':1324 }
    :return: plt object
    :usage:
    plt = draw_visitors()
    plt.show()
    """
    if len(visitor_data) == 0:
        x = ['2020.1', '2020.2', '2020.3', '2020.4', '2020.5', '2020.6', '2020.7', '2020. 8', '2020.9', '2020.10']

        y = [0, 300, 1900, 2500, 3400, 6900, 7000, 500, 1000, 12000]
        for each in x:
            index_ = x.index(each)
            visitor_data[each] = y[index_]

    label = ['visitors']
    fig, ax = plt.subplots()
    ax.stackplot(visitor_data.keys(), visitor_data.values(), labels=label, color='#EE761C')
    ax.legend(loc='upper left')
    return plt


# plt = draw_visitors()
# plt.show()


# _, iso_code = get_country_info('89.218.177.218')
# print(iso_code)


def download_flag(iso_code):
    """
    Downloads the iso flag file to the dir lifebrick/data/flags dir
    :param iso_code:
    :return:
    """
    base_url = "https://www.translatorscafe.com/cafe/images/flags/"
    full_url = base_url + iso_code + '.gif'
    flags_dir = os.path.join(lifebrick.__path__[0], 'data', 'flags')
    full_dir = os.path.join(flags_dir, f"{iso_code}.gif")
    import requests
    import shutil
    # print(full_url)
    # print(full_dir)
    r = requests.get(full_url, stream=True)
    if r.status_code == 200:
        with open(full_dir, 'wb') as f:
            for chunk in r:
                f.write(chunk)


def all_iso_codes():
    """
    Get all iso codes that life brick can handle.
    :return: list file containing all flag iso codes.
    """
    flag_iso = []
    import csv
    csv_dir = os.path.join(lifebrick.__path__[0], 'data', 'iso3166.csv')
    with open(csv_dir, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t')
        for row in spamreader:
            flag_iso.append(row[1])
            flag_iso.append(row[3])
    return flag_iso


# download all the flag images
# from lifebrick.static import flag_iso
#
# for each in flag_iso:
#     download_flag(each)
#     print(each, '0k')


def draw_visitor_country(country_data={}):
    """
    Draws the visitor country data, left side is the country code, x is the total visitors.
    :param country_data: python dictionary. {}
    :return:
    """
    if len(country_data) == 0:
        x = ['US', 'KZ', 'RU', 'TR', 'CN']
        y = [6900, 7000, 500, 1000, 12000]
        for each in x:
            index_ = x.index(each)
            country_data[each] = y[index_]

    fig, ax = plt.subplots()
    countries = country_data.keys()
    visits = country_data.values()
    y_pos = list(countries)
    ax.barh(y_pos, visits, color='#EE761C')
    return plt


def draw_price(price_data={}):
    if len(price_data) == 0:
        price_data = {
            '01.11': {
                'KZT': 2000,
                'USD': 5,
            },
            '02.13': {
                'KZT': 2200,
                'USD': 4,
            },
            '03.21': {
                'KZT': 2500,
                'USD': 3,
            },
            '04.18': {
                'KZT': 2300,
                'USD': 4,
            },
            '05.28': {
                'KZT': 2900,
                'USD': 5.5,
            },
            '06.01': {
                'KZT': 2980,
                'USD': 5.6,
            },
        }

    x_data = list(price_data.keys())
    y_data_kzt = [price_data[each]['KZT'] for each in x_data]
    y_data_usd = [price_data[each]['USD'] for each in x_data]
    plt.figure()

    plt.subplot(121)
    label = 'KZT'
    plt.plot(x_data, y_data_kzt, color='#EE761C', label=label)
    plt.legend(loc='upper left')

    plt.subplot(122)
    label = 'USD'
    plt.plot(x_data, y_data_usd, color='#EE761C', label=label)
    plt.legend(loc='upper left')

    return plt


# plt3 = draw_price()
# plt3.show()
