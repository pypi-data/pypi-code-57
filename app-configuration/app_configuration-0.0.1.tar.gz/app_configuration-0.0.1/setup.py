import setuptools
from setuptools import setup
setup(
    name = 'app_configuration',
    version = '0.0.1',
    description='Flask configuration',
    long_description_content_type='text/x-rst',
    packages = setuptools.find_packages(include=['app_configuration']),
    author= 'JuniperFag',
    license = 'MIT',
    python_requires='~=3.6'
)