import os, sys
from setuptools import find_packages, setup
from aos.managers.constant import PYURLPKG
sys.path.append('./aos')
from aos import __title__, __version__, __description__, __url__, __author__, __email__
from aos.constant import AOS_INVESTIGATION_FILE

LONG_DESC = open('pypi_readme.rst').read()
LICENSE = open('LICENSE').read()

# remove the old config file first
if os.path.isfile(AOS_INVESTIGATION_FILE):
    try:
        os.unlink(AOS_INVESTIGATION_FILE)
    except Exception as e:
        pass

install_requires = [
    'pyserial',
    'esptool',
    'scons',
    'requests',
    'click',
    'paho-mqtt',
    'progressbar2',
    'configparser',
    PYURLPKG,
]

setup(
    name=__title__,
    version=__version__,
    description=__description__,
    long_description=LONG_DESC,
    url=__url__,
    author=__author__,
    author_email=__email__,
    license=LICENSE,
    python_requires='>=2.7',
    packages=find_packages(),
    package_dir={'aos':'aos'},
    package_data={'aos': ['.vscode/*']},
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'aos=aos.__main__:main',
            'aos-cube=aos.__main__:main',
        ]
    },
)
