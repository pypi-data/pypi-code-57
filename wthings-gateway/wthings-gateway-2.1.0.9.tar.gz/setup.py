from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSION = "2.1.0.9"
setup(
    version=VERSION,
    name="wthings-gateway",
    author="WThings",
    author_email="xiaoboplus@visionet.com.cn",
    license="Apache Software License (Apache Software License 2.0)",
    description="WThings Gateway for IoT devices.",
    url="https://www.xiaobodata.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    python_requires=">=3.5",
    packages=['wthings_gateway', 'wthings_gateway.gateway', 'wthings_gateway.storage', 'wthings_gateway.logs',
              'wthings_gateway.wt_client', 'wthings_gateway.connectors', 'wthings_gateway.connectors.ble',
              'wthings_gateway.connectors.mqtt', 'wthings_gateway.connectors.opcua', 'wthings_gateway.connectors.request',
              'wthings_gateway.connectors.modbus', 'wthings_gateway.wt_utility', 'wthings_gateway.extensions',
              'wthings_gateway.extensions.mqtt', 'wthings_gateway.extensions.modbus', 'wthings_gateway.extensions.opcua',
              'wthings_gateway.extensions.ble', 'wthings_gateway.extensions.serial', 'wthings_gateway.extensions.request',
              'wthings_gateway.config',
              ],
    install_requires=[
        'cffi',
        'jsonpath-rw',
        'regex',
        'pip',
        'jsonschema==3.1.1',
        'lxml',
        'opcua',
        'paho-mqtt',
        'pymodbus',
        'Pyro4',
        'pyserial',
        'pytz',
        'PyYAML',
        'simplejson',
        'pyrsistent'
    ],
    download_url='',
    entry_points={
        'console_scripts': [
            'wthings-gateway = wthings_gateway.wt_gateway:main'
        ]
    },
    package_data={
        "": ["*.yaml", "*.conf"]
    })



