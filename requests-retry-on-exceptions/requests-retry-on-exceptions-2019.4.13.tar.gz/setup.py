from setuptools import setup

setup(
    name='requests-retry-on-exceptions',
    version='2019.4.13',
    install_requires=[
        'Requests',
        'setuptools',
        'urllib3',
    ],
    packages=[
        'requests_retry_on_exceptions',
    ],
)
