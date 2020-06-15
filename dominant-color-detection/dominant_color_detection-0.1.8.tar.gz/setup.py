# -*- encoding: utf-8 -*-
# ! python3

from setuptools import setup
from pathlib import Path

long_description = Path('README.md').open(mode='r', encoding='utf-8').read()

setup(
    name='dominant_color_detection',
    packages=['dominant_color_detection'],
    version='0.1.8',
    license='MIT',
    description='Detects dominant color of an image',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Hynek Davídek',
    author_email='hynek.davidek@biano.com',
    keywords=['image', 'color', 'detection', 'dominant', 'kmeans'],
    install_requires=['numpy', 'Pillow', 'scikit-learn'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
