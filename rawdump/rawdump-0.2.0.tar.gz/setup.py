# -*- coding: utf-8 -*-

import setuptools

import rawdump

with open('README.md') as fp:
    README = fp.read()


with open('requirements.txt') as fp:
    text = fp.read()
    REQUIREMENTS = text.split('\n')


setuptools.setup(
    author="drunkdream",
    author_email="drunkdream@qq.com",
    name='rawdump',
    license="MIT",
    description='Dump tcp/ip packet by raw socket.',
    version=rawdump.VERSION,
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/drunkdream/rawdump',
    packages=setuptools.find_packages(),
    python_requires=">=2.7",
    install_requires=REQUIREMENTS,
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: Developers',
    ],
    entry_points={
        'console_scripts': [
            'rawdump = rawdump.__main__:main',
        ],
    }
)
