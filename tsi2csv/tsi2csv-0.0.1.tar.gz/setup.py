"""setup.py -- setup script

Setuptools config
"""

from setuptools import setup


setup(
    name='tsi2csv',
    version='0.0.1',
    packages=['tsi2csv'],
    install_requires=[
        'click'
    ],
    entry_points={
       'console_scripts': [
           'tsi2csv = tsi2csv.main:cli'
       ]
    }
)
