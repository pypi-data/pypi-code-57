#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
retrieve remote XML data in CMI format
"""

import requests

from lxml import etree


def remote_file(url):
    """
    send http get request to given url
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            parser = etree.XMLParser(remove_blank_text=True)
            return etree.fromstring(response.content, parser=parser)
        print("requesting remote file failed!")
        print("url of request:")
        print(response.url)
        print("http status code: ",
              str(response.status_code))
    except requests.exceptions.ConnectionError:
        print("request failed! connection error...")
    except requests.exceptions.Timeout:
        print("request failed! timeout... try later?")
    except requests.exceptions.TooManyRedirects:
        print("request failed! bad url, try another one!")
    except requests.exceptions.RequestException:
        print("request failed! don't know why...")
    return None
