#!/usr/bin/env python

# Copyright (C) 2020 David Villa Alises
#
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from setuptools import setup

# hack to prevent 'test' target exception:
# http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html
import multiprocessing, logging

config = dict(
    name             = 'attrezzo',
    version          = '0.0.0',
    description      = 'Test doubles for Python',
    keywords         = ['unit tests', 'doubles', 'stub', 'spy', 'mock'],
    author           = 'David Villa Alises',
    author_email     = 'David.Villa@gmail.com',
    url              = 'https://github.com/davidvilla/attrezzo',
    packages         = ['attrezzo'],
    data_files       = [('', ['README.md'])],
    license          = 'GPLv3',
    )

setup(**config)
