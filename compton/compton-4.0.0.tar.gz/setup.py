import os
from setuptools import setup

from compton import __version__

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


settings = dict(
    name='compton',
    packages=[
        'compton'
    ],
    version=__version__,
    author='Kael Zhang',
    author_email='i+pypi@kael.me',
    description=('An abstract data flow framework for quantitative trading'),
    license='MIT',
    keywords='compton dataflow quant quantitative trading stock',
    url='https://github.com/kaelzhang/python-compton',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    python_requires='>=3.7',
    classifiers=[
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ]
)


if __name__ == '__main__':
    setup(**settings)
