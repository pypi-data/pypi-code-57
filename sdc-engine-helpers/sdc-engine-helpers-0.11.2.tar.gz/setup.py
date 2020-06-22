"""
    Set up the sdc_engine_helpers package
"""
from setuptools import setup

setup(
    name='sdc-engine-helpers',
    packages=[
        'sdc_engine_helpers',
        'sdc_engine_helpers.personalize',
        'sdc_engine_helpers.personalize.maintenance',
        'sdc_engine_helpers.personalize.event',
        'sdc_engine_helpers.personalize.recommendations',
        'sdc_engine_helpers.sagemaker',
        'sdc_engine_helpers.sagemaker.recommendations'
    ],
    install_requires=[
        'sdc-helpers==0.7'
    ],
    description='AWS Recommendation Engine Helpers',
    url='http://github.com/RingierIMU/sdc-recommend-engine-helpers',
    version='0.11.2',
    author='Ringier South Africa',
    author_email='tools@ringier.co.za',
    keywords=[
        'pip',
        'helpers',
        'aws',
        'recommendation',
        'personalize',
        'sageMaker'
    ],
    download_url='https://github.com/RingierIMU/sdc-recommend-engine-helpers/archive/v0.11.2.zip'
)
