import setuptools
from sys import version

if version < '2.2.3':
	from distutils.dist import DistributionMetadata
	DistributionMetadata.classifiers = None
	DistributionMetadata.download_url = None
	
from distutils.core import setup


setuptools.setup(
                    name='sfws',
                    version='2.0.1',
                    author='@rockscripts',
                    author_email='rockscripts@gmail.com',
                    description='SF Company',
                    long_description="SF Company",
                    install_requires=[],
                    platforms='any',
                    url='http://odoo.com',
                    packages=['sfws'],
                    python_requires='>=2.7.*',
                    classifiers=[
                                    'License :: OSI Approved :: BSD License',
                                    'Programming Language :: Python :: 3',
                                    'Topic :: Software Development :: Libraries :: Python Modules',
                                ],
                )