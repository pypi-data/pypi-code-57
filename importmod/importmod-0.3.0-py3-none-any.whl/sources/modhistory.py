# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""Utility functions for interacting with mw.modhistory.com"""

import requests

from bs4 import BeautifulSoup


def get_modhistory_info(url):
    """
    Returns information in the hompage for the given modhistory mod

    Generally contains the following fields:
    Version, Added, Last Edited, File Size, Downloads, Requires, Submitted by
    """
    rinfo = requests.get(url)
    if rinfo.status_code != requests.codes.ok:
        rinfo.raise_for_status()

    soup = BeautifulSoup(rinfo.text)
    data = {}
    for elem in soup.find_all("td"):
        info = elem.find_all("span")
        if info and len(info) >= 2:
            title = info[0].string.rstrip(":")
            value = info[1].string
            data[title] = value
    return data
