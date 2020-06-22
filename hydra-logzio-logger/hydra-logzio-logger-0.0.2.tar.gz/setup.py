from pip._internal.network.session import PipSession
from pip._internal.req import parse_requirements

import setuptools

from hydra_plugins import hydra_logzio_logger

install_reqs = parse_requirements('requirements.txt', session=PipSession)

with open("README.md", "r") as fh:
   long_description = fh.read()

setuptools.setup(
   name='hydra-logzio-logger',
   version=hydra_logzio_logger.__version__,
   description='hydra-logzio-logger, hydra plugin to log into logzio server',
   long_description=long_description,
   long_description_content_type="text/markdown",
   url="https://github.com/shay-te/hydra-logzio-logger",
   setup_requires=['wheel'],
   author='Shay Tessler',
   author_email='shay.te@gmail.com',
   packages=setuptools.find_packages(),
   include_package_data=True,
   install_requires=[str(ir.requirement) for ir in install_reqs],
   license="MIT",
   classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
   ],
   python_requires='>=3.7'
)