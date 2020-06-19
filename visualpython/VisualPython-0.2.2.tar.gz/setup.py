# coding: utf-8
import os
#from distutils.core import setup
#from distutils.command.build_py import build_py
#from distutils.command.sdist import sdist
#from os.path import join as pjoin

from setuptools import setup, find_packages

name = 'VisualPython'

setup(
    name             = name,
    version          = '0.2.2',
    packages         = find_packages(),
    package_data     = { 'visualpython' : ['Main.js', 'visualpython.yaml', 'MainLayout.html','README.md']},
    description      = 'VisualPython',
    license          = '',
    author           = 'BlackLogic',
    author_email     = 'blacklogic.dev@gmail.com',
    url              = 'https://gitlab.com/blacklogic.dev/visualpython',
    install_requires = [],
    platforms        = "Linux, Mac OS X, Windows",
    keywords         = ['Visual', 'visual', 'VisualPython', 'visualpython'],
    classifiers      = ['Programming Language :: Python :: 3.6',
                        'Programming Language :: Python :: 3.7']
    )
