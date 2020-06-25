import importlib
try:
    importlib.import_module('numpy')
except ImportError:
	from pip._internal import main as _main
	_main(['install', 'numpy'])

from setuptools import setup, Extension, find_packages
import setuptools
import numpy
import sys
import os
from distutils.sysconfig import get_python_lib
import shutil

# To use a consistent encoding
from codecs import open

from os import path
here = path.abspath(path.dirname(__file__))

sfc_module = Extension('igeGameAnalytics',
                    sources=[
                        'igeGameAnalytics.cpp',
                        'GAnalytics.cpp',
                        'win32/GameAnalyticsImpl.cpp',
                    ],
                    include_dirs=['./', './win32', './bin/include'],
                    library_dirs=['bin/win32-vc141-mt-static/Release'],
			        libraries=['GameAnalytics', 'libcurl', 'libssl', 'libcrypto', 'advapi32', 'ws2_32', 'crypt32', 'rpcrt4', 'ole32', 'kernel32', 'user32', 'gdi32', 'winspool', 'shell32', 'oleaut32', 'uuid', 'comdlg32'])

setup(name='igeGameAnalytics', version='0.0.2',
		description= 'C++ extension GameAnalytics for 3D and 2D games.',
		author=u'Indigames',
		author_email='dev@indigames.net',
		packages=find_packages(),
		ext_modules=[sfc_module],
		long_description=open(path.join(here, 'README.md')).read(),
        long_description_content_type='text/markdown',
        
        # The project's main homepage.
        url='https://indigames.net/',
        
		license='MIT',
		classifiers=[
			'Intended Audience :: Developers',
			'License :: OSI Approved :: MIT License',
			'Programming Language :: Python :: 3',
			#'Operating System :: MacOS :: MacOS X',
			#'Operating System :: POSIX :: Linux',
			'Operating System :: Microsoft :: Windows',
			'Topic :: Games/Entertainment',
		],
        # What does your project relate to?
        keywords='GameAnalytics 3D game Indigames',
      )
