# package製作
# python setup.py sdist
# twine upload --verbose dist/LazyPyUtil-0.1.0.tar.gz

import os
import setuptools

with open('requirements.txt') as fid:
    requires = [line.strip() for line in fid]

setuptools.setup(
    name='LazyPyUtil',
    version='0.1.0',
    description="Woody's Lazy Python Utility",
    keywords = ['ccy1219','utility','library'],
    author='Woody Chen',
    author_email='ccy1219@gmail.com',
    install_requires=requires,
    packages=setuptools.find_packages(),
    platforms='any',
    license='MIT',
    url='https://github.com/ccy1219/LazyPyUtil'
)
