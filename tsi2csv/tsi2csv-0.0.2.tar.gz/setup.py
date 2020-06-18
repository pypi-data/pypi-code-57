"""setup.py -- setup script

Setuptools config
"""

from setuptools import setup


setup(
    name='tsi2csv',
    version='0.0.2',
    author='Richard T. Carback III',
    author_email='rick.carback@gmail.com',
    description='Convert from LinkedOmics multi-omics tsi data format to csv',
    url='https://gitlab.com/carback1/tsi2csv',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
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
