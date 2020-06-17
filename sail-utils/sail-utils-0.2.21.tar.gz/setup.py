import io
from setuptools import setup
from setuptools import find_packages

setup(
    name='sail-utils',
    version='0.2.21',
    packages=find_packages(),
    install_requires=io.open('requirements.txt', encoding='utf8').read(),
    url='',
    license='',
    author='',
    author_email='',
    description=''
)
