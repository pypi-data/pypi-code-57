#!/usr/bin/python

from setuptools import setup
from setuptools import find_packages

# reading long description from file
with open('README.md') as file:
    long_description = file.read()


# specify requirements of your package here
REQUIREMENTS = []

# some more details
CLASSIFIERS = [
    "Operating System :: OS Independent",
    'Intended Audience :: Developers',
    'Topic :: Internet',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
	]

# calling the setup function
setup(name='splicejunxchx',
      version='2.0',
      description='characterize the splice junctions outputted by SJ.out.tab file',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Ayush Kumar',
      author_email='ayush.kumar@umassmed.edu',
      license='MIT',
      url = 'https://github.com/ayushkumar-umms/splice-junction-characterization',
      packages=find_packages(),
      entry_points = {
        'console_scripts': [
            'splicejunxchx = splicejunxchx.splicejunxchx:main'
        ]
      },
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      python_requires='>=3.6',
      keywords='splicing',
      )

