from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fasten',
    version='0.0.3',
    description='Fasten Plug-ins basic interface',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    author='',
    author_email='',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='',
    packages=find_packages(),
    python_requires='>=3.4, <4',
    install_requires=['kafka-python>=2.0.1'],
)
