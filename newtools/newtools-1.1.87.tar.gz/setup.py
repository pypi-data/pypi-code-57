"""
(c) Dativa 2012-2020, all rights reserved

This code is licensed under MIT license (see license.txt for details)
"""
import os
from setuptools import setup

with open('README.md') as f:
    long_description = f.read()


def get_version():
    return open('version.txt', 'r').read().strip()


with open(os.path.join(os.path.split(__file__)[0], 'requirements.txt')) as f:
    reqs = f.readlines()

setup(name='newtools',
      version=get_version(),
      description='A selection of tools for easier processing of data using Pandas and AWS',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://bitbucket.org/dativa4data/newtools/',
      author='Dativa',
      author_email='hello@dativa.com',
      license='MIT',
      zip_safe=False,
      packages=['newtools',
                'newtools.aws',
                'newtools.db',
                'newtools.doggo',
                'newtools.log'],
      include_package_data=True,
      setup_requires=[
          'setuptools>=41.0.1',
          'wheel>=0.33.4',
          'numpy>=1.13.3'],
      extras_require={
          "full": reqs
      },
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers',
                   'Topic :: Software Development :: Libraries',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3.7'],
      keywords='dativa', )
