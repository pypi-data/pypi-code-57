#!/usr/bin/python
import versioneer
from setuptools import setup, find_packages


setup(
    name='sdccli',
    author='sysdig Inc.',
    author_email='info@sysdig.com',
    license='MIT',
    description='CLI client for Sysdig Cloud',
    url='https://github.com/draios/sysdig-platform-cli',
    packages=find_packages(exclude=['test', 'specs', 'specs.*']),
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    entry_points='''
    [console_scripts]
    sdc-cli=sdccli.cli:cli
    ''',
    install_requires=['click', 'python-dateutil', 'prettytable', 'pyyaml', 'requests', 'sdcclient'],
    test_suite="test"
)
