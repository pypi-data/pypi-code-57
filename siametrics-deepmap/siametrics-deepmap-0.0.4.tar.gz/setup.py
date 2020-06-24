import  setuptools
from setuptools import setup


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='siametrics-deepmap',
    version='0.0.4',
    packages=setuptools.find_packages(),
    url='',
    license='Apache 2.0',
    author='SSripilaipong',
    author_email='santhapon.s@siametrics.com',
    description='',
    python_requires='>=3.6',
    install_requires=requirements,
)
