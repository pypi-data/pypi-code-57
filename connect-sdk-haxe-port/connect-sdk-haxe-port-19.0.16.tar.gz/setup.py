from os import path
from setuptools import setup


with open(path.join(path.abspath(path.dirname(__file__)), 'README.md')) as fhandle:
    README = fhandle.read()


setup(
    name='connect-sdk-haxe-port',
    version='19.0.16',
    description='CloudBlue Connect SDK, generated from Haxe',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Ingram Micro',
    author_email='connect-service-account@ingrammicro.com',
    keywords='connect sdk cloudblue ingram micro ingrammicro cloud automation',
    packages=['connect', 'connect.api', 'connect.logger', 'connect.models', 'connect.storage', 'connect.util'],
    url='https://github.com/cloudblue/connect-haxe-sdk',
    license='Apache Software License',
    install_requires=['requests==2.21.0']
)
