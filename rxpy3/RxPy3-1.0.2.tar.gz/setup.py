#!/usr/bin/env python3

import sys 

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

from configparser import ConfigParser


# General project metadata is stored in project.cfg
with open('project.cfg') as project_file:
    config = ConfigParser()
    config.read_file(project_file)
    project_meta = dict(config.items('project'))


# Populate the long_description field from README.rst
with open('README.rst') as readme_file:
    project_meta['long_description'] = readme_file.read()


needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

setup(
    **{key: project_meta[key] for key in (
        'name',
        'version',
        'description',
        'long_description',
        'author',
        'author_email',
        'license',
        'url',
        'download_url'
    )},
    zip_safe=False,
    python_requires='>=3.6.0',

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    setup_requires=pytest_runner,
    tests_require=['pytest>=4.6.1', 'pytest-asyncio>=0.10.0', 'coverage>=4.5.3'],

    package_data={'rx3': ['py.typed']},
    packages=['rx3', 'rx3.internal', 'rx3.core', 'rx3.core.abc',
              'rx3.core.operators', 'rx3.core.operators.connectable',
              'rx3.core.observable', 'rx3.core.observer',
              'rx3.scheduler', 'rx3.scheduler.eventloop', 'rx3.scheduler.mainloop',
              'rx3.operators', 'rx3.disposable', 'rx3.subject',
              'rx3.testing'],
    package_dir={'rx3': 'rx3'},
    include_package_data=True
)
