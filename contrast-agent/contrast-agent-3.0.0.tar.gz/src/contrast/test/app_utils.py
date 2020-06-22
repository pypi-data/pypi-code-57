# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Common code for test applications
"""


def getitem_request(request, key, default=""):
    if request.method == "GET":
        param = request.GET
    elif request.method == "POST":
        param = request.POST
    else:
        return default

    try:
        return param[key]
    except KeyError:
        return default
