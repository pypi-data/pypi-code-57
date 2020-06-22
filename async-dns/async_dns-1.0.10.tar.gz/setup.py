# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['async_dns',
 'async_dns.core',
 'async_dns.core.config',
 'async_dns.resolver',
 'async_dns.server']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'async-dns',
    'version': '1.0.10',
    'description': 'Asynchronous DNS client and server',
    'long_description': "# async_dns\n\n[![PyPI](https://img.shields.io/pypi/v/async_dns.svg)]()\n\nAsynchronous DNS server and client built with pure Python.\n\nRequirements: Python 3.5+ (`asyncio` is required).\n\n## Installation\n\n``` sh\n$ pip3 install async_dns\n# or\n$ pip3 install git+https://github.com/gera2ld/async_dns.git\n```\n\n## CLI\n\n### Resolver\n```\nusage: python3 -m async_dns.resolver [-h] [-p {udp,tcp}]\n                                     [-n NAMESERVERS [NAMESERVERS ...]]\n                                     [-t TYPES [TYPES ...]]\n                                     hostnames [hostnames ...]\n\nAsync DNS resolver\n\npositional arguments:\n  hostnames             the hostnames to query\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -p {udp,tcp}, --protocol {udp,tcp}\n                        whether to use TCP protocol as default to query remote\n                        servers\n  -n NAMESERVERS [NAMESERVERS ...], --nameservers NAMESERVERS [NAMESERVERS ...]\n                        name servers\n  -t TYPES [TYPES ...], --types TYPES [TYPES ...]\n                        query types, default as `any`\n```\n\nExamples:\n``` sh\n# Resolve an IP\n$ python3 -m async_dns.resolver www.google.com\n$ python3 -m async_dns.resolver -t mx -- gmail.com\n\n# Query via TCP\n$ python3 -m async_dns.resolver -n 127.0.0.1 -p tcp www.google.com\n```\n\n### Server\n```\nusage: python3 -m async_dns.server [-h] [-b BIND] [--hosts HOSTS]\n                                   [-P PROXY [PROXY ...]] [-p {udp,tcp}]\n\nDNS server by Gerald.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -b BIND, --bind BIND  the address for the server to bind\n  --hosts HOSTS         the path of a hosts file\n  -x PROXY [PROXY ...], --proxy PROXY [PROXY ...]\n                        the proxy DNS servers, `none` to serve as a recursive\n                        server, `default` to proxy to default nameservers\n  -p {udp,tcp}, --protocol {udp,tcp}\n                        whether to use TCP protocol as default to query remote\n                        servers\n```\n\nExamples:\n``` sh\n# Start a DNS proxy server on :53 via TCP\n$ python3 -m async_dns.server -b :53 -p tcp --hosts /etc/hosts\n\n# Start a DNS server over TCP proxy\n$ python3 -m async_dns.server -x 8.8.8.8 -p tcp\n\n# Start a DNS recursive server\n$ python3 -m async_dns.server -x none\n```\n\n## API\n\n``` python\nimport asyncio\nfrom async_dns import types\nfrom async_dns.resolver import ProxyResolver\n\nloop = asyncio.get_event_loop()\nresolver = ProxyResolver()\nres = loop.run_until_complete(resolver.query('www.baidu.com', types.A))\nprint(res)\n```\n\nProxyResolver supports routing based on domains:\n\n```python\nresolver = ProxyResolver(proxies=[\n    ('*.lan', ['192.168.1.1']),                        # query '192.168.1.1' for '*.lan' domains\n    (lambda d: d.endswith('.local'), ['127.0.0.1']),   # query 127.0.0.1 for domains ending with '.local'\n    (None, ['8.8.8.8', '8.8.4.4']),                    # None matches all others\n])\n```\n\n## Test\n\n``` sh\n$ python3 -m unittest\n```\n",
    'author': 'Gerald',
    'author_email': 'i@gerald.top',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gera2ld/async_dns',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
