from setuptools import setup

setup(
    name='pypi-simple-iter',
    version='2019.4.14',
    install_requires=[
        'Requests',
        'pypi_slug',
        'requests_retry_on_exceptions',
        'setuptools',
    ],
    packages=[
        'pypi_simple_iter',
    ],
)
