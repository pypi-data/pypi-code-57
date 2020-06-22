from os import path
import sys

import geoip2.database
import requests


__version__ = '0.20200616.2'


def main(domain, provider=None):
    ipa = resolve(domain, provider)
    reader = geoip2.database.Reader(
        path.join(
            path.dirname(__file__),
            f'GeoLite2-Country_{__version__[2:-2]}/GeoLite2-Country.mmdb'
        )
    )
    response = reader.country(ipa)
    return response.country.iso_code


def resolve(domain_name, provider=None):
    for answer in doh({'name': domain_name}, provider)['Answer']:
        if answer['type'] == 1:
            return answer['data']
    for answer in doh({'name': domain_name}, provider)['Answer']:
        if answer['type'] == 5:
            return resolve(answer['data'], provider)
    raise Exception


def doh(params, provider=None):
    provider = provider or cloudflare
    try:
        res = provider(params)
    except TypeError:
        res = {
            'ali': ali, 'cloudflare': cloudflare, 'google': google
        }[provider.strip().lower()](params)
    res.raise_for_status()
    return res.json()


def ali(params):
    return requests.get('https://dns.alidns.com/resolve', params=params)


def cloudflare(params):
    return requests.get(
        'https://cloudflare-dns.com/dns-query',
        params=params,
        headers={'accept': 'application/dns-json'}
    )


def google(params):
    return requests.get('https://dns.google/resolve', params=params)


if __name__ == '__main__':
    print(main(sys.argv[1], sys.argv[2]))
