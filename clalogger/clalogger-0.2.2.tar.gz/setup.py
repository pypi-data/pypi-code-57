"""Distutil's setup.py"""

import os
import pathlib
import setuptools as stt
import sys

_SETUP_DIR = pathlib.Path(sys.argv[0]).parent.resolve()
_VERSION = "0.2"  # sphinx: version and release; not used for wheels
_RELEASE = ".".join([_VERSION, "2"])  # used for wheel and sphinx
_NAME = "clalogger"
_GITHUB = 'https://github.com/mhooreman/clalogger'
_AUTHOR = 'Michaël Hooreman'
_COPYRIGHT = '2019-2020, %s' % _AUTHOR
_LICENSE = 'MIT'


def _getLongDescription():
    with open(_SETUP_DIR.joinpath('README.rst'), 'r') as fh:
        return fh.read()


def _setup():
    stt.setup(
        name=_NAME,
        version=_RELEASE,
        description='Logging from class point of view, with easy config',
        long_description=_getLongDescription(),
        long_description_content_type='text/markdown',
        license=_LICENSE,
        url=_GITHUB,
        author=_AUTHOR,
        author_email='michael@hooreman.be',
        classifiers=[  # https://pypi.org/classifiers/
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.7',
        ],
        keywords='logging stacktrace caller',
        package_dir={'': 'src'},
        packages=stt.find_packages(where='src'),
        include_package_data=True,
        install_requires=None,
        setup_requires=None,
        python_requires='>=3.6',
        extras_require=None,
        project_urls={
            'Source': _GITHUB,
        },
    )


def _main():
    os.chdir(pathlib.Path(__file__).parent)
    _setup()


if __name__ == "__main__":
    _main()
