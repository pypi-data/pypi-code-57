from setuptools import setup


setup(
    name             = 'Torrelque',
    version          = '0.3.1',
    author           = 'saaj',
    author_email     = 'mail@saaj.me',
    packages         = ['torrelque'],
    license          = 'LGPL-3.0-only',
    description      = 'Asynchronous Redis-backed reliable queue package',
    long_description = open('README.rst', 'rb').read().decode('utf-8'),
    platforms        = ['Any'],
    keywords         = 'python redis asynchronous reliable-queue work-queue',
    project_urls     = {
        'Source Code'   : 'https://heptapod.host/saajns/torrelque',
        'Documentation' : 'https://torrelque.readthedocs.io/',
    },
    classifiers = [
        'Topic :: Software Development :: Libraries',
        'Framework :: AsyncIO',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Intended Audience :: Developers'
    ],
    install_requires = ['aredis >= 1.1, < 2'],
    extras_require   = {
        'test'   : ['asynctest < 0.14'],
        'manual' : ['sphinx >= 3, < 4'],
    },
)
