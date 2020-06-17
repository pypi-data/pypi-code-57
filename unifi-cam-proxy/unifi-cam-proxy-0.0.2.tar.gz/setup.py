#!/usr/bin/env python

from distutils.core import setup
from unifi import version

setup(
    name = 'unifi-cam-proxy',
    packages = ["unifi"],
    version = version.__version__,
    description = 'Unifi NVR-compatible camera proxy',
    long_description = open('README.md').read(),
    author = 'Keshav Varma',
    entry_points = {
        'console_scripts': ['unifi-cam-proxy=unifi.main:main'],
    },
    url = 'https://github.com/keshavdv/unifi-cam-proxy',
    install_requires = [
        "coloredlogs",
        "requests",
        "websocket-client",
        "flvlib",
        "hikvisionapi",
        "xmltodict",
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
    ],
)
