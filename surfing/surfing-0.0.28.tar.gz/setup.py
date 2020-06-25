from setuptools import setup, find_packages
from surfing import __version__
import os

curr_dir = os.path.split(os.path.abspath(__file__))[0]
requirements = open(os.path.join(curr_dir, 'requirements.txt')).readlines()
requirements = [p.strip('\n') for p in requirements]
requirements = [p for p in requirements if p]

setup(
    name='surfing',
    version=__version__,
    description='backtest engine',
    author='puyuantech',
    author_email='info@puyuan.tech',
    packages=find_packages(),
    install_requires=requirements
)

#python3 setup.py bdist_egg --exclude-source-files --dist-dir=../