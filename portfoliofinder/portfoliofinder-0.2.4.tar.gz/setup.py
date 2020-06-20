"""
Setup Script
"""

import re
from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open("portfoliofinder/__init__.py", "r") as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    ).group(1)

setup(name='portfoliofinder',
      version=version,
      description='Tool to help find an optimal portfolio allocation',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/asteffey/portfolio-finder',
      author='Andrew Steffey',
      author_email='asteffey@gmail.com',
      license='MIT',
      packages=['portfoliofinder'],
      install_requires=[
          'pandas',
          'dill',
          'matplotlib',
          'mplcursors',
          'numpy',
          'progressbar2',
          'scipy'
      ],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8'
      ],
      zip_safe=False)
