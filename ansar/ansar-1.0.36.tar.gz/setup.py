# Standard PyPi packaging.
# Build materials and push to pypi.org.
# Author: Scott Woods <scott.suzuki@gmail.com>
from setuptools import setup

MAJOR_MINOR='major_minor'
BUILD_NUMBER='build_number'
SEMANTIC_VERSION='%d.%d.%s'
DOWNLOAD_URL='https://gitlab.com/scott.ansar/ansar/archive/%s.tar.gz'
README='README.rst'

# Load major and minor version numbers from
# file storage. This file should be created by
# pipeline from pipeline variables.
mm = open(MAJOR_MINOR, "r")
line = mm.readline().strip()
line = line.split('.')
major = int(line[0].strip())
minor = int(line[1].strip())
mm.close()

bn = open(BUILD_NUMBER, "r")
build = bn.readline().strip()
bn.close()

# Combine environment and auto-increment numbers to
# create strings for setup.
semantic_version=SEMANTIC_VERSION % (major, minor, build)
download_url=DOWNLOAD_URL % (semantic_version,)

#
#
rm = open(README, 'r')
readme = rm.read()

setup(
    name = 'ansar',
    packages = ['ansar'],   # 'cli'
    version = semantic_version,
    description = 'Storing and recovering application objects.',
    long_description = readme,
    author = 'Scott Woods',
    author_email = 'scott.suzuki@gmail.com',
    url= 'https://gitlab.com/scott.ansar/ansar',
    download_url=download_url,
    keywords = ['serialization', 'persistence'], # arbitrary keywords
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = 'defusedxml >= 0.6',
    #entry_points={
    #    "console_scripts": [
    #        'ansar=cli.entry_ansar:main',
    #        'ansar-group=cli.entry_group:main',
    #        'ansar-lan=cli.entry_lan:main',
    #    ]
    #}
)
