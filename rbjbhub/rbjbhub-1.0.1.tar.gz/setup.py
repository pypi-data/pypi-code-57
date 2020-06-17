#!/usr/bin/env python

from __future__ import unicode_literals

from reviewboard.extensions.packaging import setup
from setuptools import find_packages


setup(
    name='rbjbhub',
    version='1.0.1',
    author='Gary Kramlich',
    author_email='grim@reaperworld.com',
    url='https://keep.imfreedom.org/grim/reviewboard_jetbrains_hub',
    description='JetBrains Hub Support for ReviewBoard',
    packages=find_packages(),
    install_requires=['requests'],
    entry_points={
        'reviewboard.extensions': [
            'jbhub = rbjbhub.extension:JetBrainsHubExtension',
        ],
    },
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Review Board',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    ],
)
