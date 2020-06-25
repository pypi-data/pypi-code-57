"""
    Set up the sdc_helpers package
"""
from setuptools import setup
import os


def get_required(file_name):
    with open(file_name) as f:
        return f.read().splitlines()


setup(
    name='sdc_dp_helpers',
    packages=
    [
        'sdc_dp_helpers',
        'sdc_dp_helpers.google_analytics',
        'sdc_dp_helpers.api_utilities',
    ],
    install_requires=get_required(file_name='./requirements.txt'),
    description='A module for developing data pipelines from external api\'s',
    version='0.2.1',
    url='http://github.com/RingierIMU/sdc-dataPipeline-helpers',
    author='Ringier South Africa',
    author_email='tools@ringier.co.za',
    keywords=[
        'pip',
        'datapipeline',
        'helpers',
    ]
)
