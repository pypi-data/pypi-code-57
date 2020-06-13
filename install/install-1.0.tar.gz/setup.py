import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "install",
    version = "1.0",
    author = "Eugene Kolo",
    author_email = "eugene@kolobyte.com",
    description = ("Be careful what you type out there."),
    license = "MIT",
    keywords = "install packages from within code",
    url = "https://pypi.python.org/pypi/install",
    packages=['install'],
    scripts=['bin/install'],
    long_description=read('README'),
    classifiers=[],
)
