#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'aioredis==1.3.1'
]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Aaron Yang",
    author_email='code@jieyu.ai',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="轻量级的异步消息通信，支持进程内消息通信，以及基于REDIS PUBSUB的远程消息。提供了进一步封装RPC的底层机制。",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pyemit',
    name='pyemit',
    packages=find_packages(include=['pyemit', 'pyemit.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/hbaaron/pyemit',
    version='0.4.5',
    zip_safe=False,
)
