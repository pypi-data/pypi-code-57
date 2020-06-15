import sys
import uuid
from .api import yelp
from .api import geolocation
import geocoder
import os
import click
import pprint
import time
from pydoc import pipepager
from termcolor import colored, cprint
from colorama import Fore, Back, Style

@click.command()
@click.option('--term', default='Restaurants', type=click.STRING)
@click.option('--location', default='San Francisco', type=click.STRING)
@click.option('--latitude', type=click.FLOAT)
@click.option('--longitude', type=click.FLOAT)
@click.option('--radius', default=5000, type=click.INT)
@click.option('--categories', default="", type=click.STRING)
@click.option('--locale', default="en_US", type=click.STRING)
@click.option('--limit', default=20, type=click.INT)
@click.option('--sort-by', default='best_match', type=click.STRING)
@click.option('--price', type=click.INT)
@click.option('--attributes', type=click.STRING)
def search(term, location, latitude, longitude, radius, categories, locale, limit, sort_by, price, attributes):
    print(term, location, latitude, longitude, radius)
    
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'latitude': latitude,
        'longitude': longitude,
        'radius': radius,
        'categories': categories,
        'locale': locale,
        'limit': limit,
        'sort-by': sort_by,
        'price': price,
        'attributes': attributes,
    }
    
    if not latitude and not longitude:
        # using google maps geolocation API if you have a key
        if 'GOOGLE_API_KEY' in os.environ:
            print('using Google API')
            geo = geolocation.geolocate()
            print(geo)
            url_params['latitude'] = geo['location']['lat']
            url_params['longitude'] = geo['location']['lng']
        else:
            # uses this inaccurate api as test
            print('using geocoder')
            g = geocoder.ip('me')
            print(g.latlng)
    
    bus = yelp.query_api(url_params)

    pprint.pprint(bus[0])
    
    # for i in range(len(bus)):
    #     # print(businesses[i])
    #     print(bus[i]['name'])

    # pipepager(Fore.RED + str(bus), cmd='less -R')

@click.group()
def welp():
    pass

welp.add_command(search)
