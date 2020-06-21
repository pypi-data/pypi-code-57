from setuptools import setup, dist
from setuptools.command.install import install
import os

class BinaryDistribution(dist.Distribution):
    def has_ext_modules(foo):
        return True

this_directory = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(this_directory, 'README.md')) as fh:
    long_description = fh.read()

setup(
    name="gdistance",
    version="1.0.4",
    author="Robert Ohuru",
    author_email="robertohuru@gmail.com",
    description="Python package for the gdistance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/robertohuru/gdistance",
    packages=["gdistance"],
    package_data={"gdistance": ["_core.cp37-win_amd64.pyd"]},
	#data_files=[('gdistance', ['_core.cp37-win_amd64.pyd'])],
    include_package_data=True,
    distclass=BinaryDistribution,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
)