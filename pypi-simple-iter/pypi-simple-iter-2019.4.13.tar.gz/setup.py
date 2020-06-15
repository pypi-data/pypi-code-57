try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='pypi-simple-iter',
    version='2019.4.13',
    packages=[
        'pypi_simple_iter',
    ],
)
