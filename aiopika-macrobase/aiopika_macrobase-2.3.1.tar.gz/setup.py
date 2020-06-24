from setuptools import setup, find_packages

setup(
    name='aiopika_macrobase',
    version='2.3.1',
    packages=find_packages(),
    url='https://github.com/mbcores/aiopika-macrobase',
    license='MIT',
    author='Alexey Shagaleev',
    author_email='alexey.shagaleev@yandex.ru',
    description='Aio-pika driver for macrobase framework',
    install_requires=[
        'macrobase-driver>=2.0.0,<3.0.0',
        'aio-pika==5.5.3',
        'uvloop==0.14.0',
        'python-rapidjson==0.8.0',
        'structlog==19.2.0',
        'sentry-sdk>=0.14.3',
        'aiocontextvars==0.2.2'
    ]
)
