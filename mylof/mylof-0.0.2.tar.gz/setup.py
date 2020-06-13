# -*- coding: UTF-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mylof",
    version="0.0.2",
    author="RL",
    author_email="",
    description="A package for LOFTER users to archive their own creation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Raye2333/save_my_lofter",
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',

    ]
)
