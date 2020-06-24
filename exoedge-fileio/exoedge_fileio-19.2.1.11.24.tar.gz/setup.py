""" Installation script for ExoEdge Source. """
# pylint: disable=I0011,W0312,C0410

import os
from setuptools import setup, find_packages

REQUIREMENTS = ['exoedge']

def read(fname):
    """ Primarily used to open README file. """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# safely get the CALVER version number without having to import it
VERSION = {}
with open("exoedge_fileio/__version__.py") as fp:
    exec(fp.read(), VERSION) # pylint: disable=W0122
    assert VERSION.get('__version__'), "Unable to parse version from exoedge_file_io/__version__.py."

try:
    README = read('README.rst')
except:
    README = 'README Not Found'

setup(
    name="exoedge_fileio",
    version=VERSION['__version__'],
    author="Exosite LLC",
    author_email="support@exosite.com",
    description="An ExoEdge source for <keep this to one line>.",
    license="Apache 2.0",
    keywords="murano exosite iot iiot client gateway <!!!ADD/REMOVE/EDIT TAGS!!!>",
    url="https://github.com/exosite/lib_exoedge_file_io_python",
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    long_description=README,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Operating System Kernels :: Linux",
        "Topic :: Software Development :: Embedded Systems",
        "License :: OSI Approved :: Apache Software License",
    ],
)
