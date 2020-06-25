"""
    Set up the sdc_helpers package
"""
from setuptools import setup

setup(
    name='sdc_dp_helpers',
    packages=
    [
        'sdc_dp_helpers',
        'sdc_dp_helpers.google_analytics',
        'sdc_dp_helpers.api_utilities',
    ],
    install_requires=[
        'httplib2',
        'pathlib',
        'oauth2client',
        'numpy',
        'pandas'
    ],
    description='A module for developing data pipelines from external api\'s',
    version='0.3.1',
    url='http://github.com/RingierIMU/sdc-dataPipeline-helpers',
    author='Ringier South Africa',
    author_email='tools@ringier.co.za',
    keywords=[
        'pip',
        'datapipeline',
        'helpers',
    ]
)
