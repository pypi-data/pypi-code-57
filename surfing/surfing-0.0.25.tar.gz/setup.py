from setuptools import setup, find_packages
from surfing import __version__


setup(
    name='surfing',
    version=__version__,
    description='backtest engine',
    author='traders.link',
    author_email='info@puyuan.tech',
    packages=find_packages()
)

#python3 setup.py bdist_egg --exclude-source-files --dist-dir=../