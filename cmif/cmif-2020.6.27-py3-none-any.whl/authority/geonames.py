#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search or retrieve GeoNames

you need to set the environment variable GEO_USER like this:

  $ export GEO_USER=[my-geonames-account-username]

or pass the variable username as parameter to the functions!
"""

import os
import requests

GEODATA = "http://api.geonames.org/getJSON"
GEOSEARCH = "http://api.geonames.org/searchJSON"


def request(geoname_id, style="full", lang=None, username=None):
    """request GeoNames entity by given id (requires GeoNames username)"""
    if username is None:
        try:
            username = os.environ["GEO_USER"]
        except KeyError:
            print("")
            print("to get the GeoNames JSON data either pass")
            print("your GeoNames username like this:")
            print("getJSON(\""+geoname_id+"\", username=USERNAME)\n")
            print("... or set environment variable GEO_USER")
            print("to your GeoNames username!")
            print("")
            return None
    params = {}
    params["geonameId"] = geoname_id
    params["style"] = style
    if lang is not None:
        params["lang"] = lang
    params["username"] = username
    try:
        result = requests.get(GEODATA, params=params).json()
    except requests.exceptions.ConnectionError:
        print("cmif.authority.geonames.request:")
        print("request failed! connection error...")
        return {}
    except requests.exceptions.Timeout:
        print("cmif.authority.geonames.request:")
        print("request failed! timeout... try later?")
        return {}
    except requests.exceptions.TooManyRedirects:
        print("cmif.authority.geonames.request:")
        print("request failed! bad url, try another one!")
        return {}
    except requests.exceptions.RequestException:
        print("cmif.authority.geonames.request:")
        print("request failed! don't know why...")
        return {}
    if "status" in result:
        print("failed to request GeoNames data!")
        print(result["status"]["message"])
        return {}
    return result


def search(place, bias="DE", username=None):
    """search GeoNames entity for given place (requires GeoNames username)"""
    if username is None:
        try:
            username = os.environ["GEO_USER"]
        except KeyError:
            print("")
            print("to do the GeoNames search either pass")
            print("your GeoNames username like this:")
            print("search(\""+place+"\", username=USERNAME)\n")
            print("... or set environment variable GEO_USER")
            print("to your GeoNames username!")
            print("")
            return None
    params = {}
    params["q"] = place
    params["username"] = username
    params["countryBias"] = bias
    params["style"] = "short"
    params["maxRows"] = 3
    try:
        result = requests.get(GEOSEARCH, params=params).json()["geonames"]
    except requests.exceptions.ConnectionError:
        print("cmif.authority.geonames.search:")
        print("request failed! connection error...")
        return "", ""
    except requests.exceptions.Timeout:
        print("cmif.authority.geonames.search:")
        print("request failed! timeout... try later?")
        return "", ""
    except requests.exceptions.TooManyRedirects:
        print("cmif.authority.geonames.search:")
        print("request failed! bad url, try another one!")
        return "", ""
    except requests.exceptions.RequestException:
        print("cmif.authority.geonames.search:")
        print("request failed! don't know why...")
        return "", ""
    if result == []:
        print("no results for given query!")
        return "", ""
    result = result[0]
    geoname = result["toponymName"]
    geonameId = "http://www.geonames.org/{0}".format(result["geonameId"])
    return geoname, geonameId
