from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
#with open(path.join(here, 'README.md'), encoding='utf-8') as f:
#    long_description = f.read()

setup(
    name='SOPRANOS',
    version='0.0.18',
    description='development version',
    #long_description=long_description,
    #long_description_content_type='text/markdown',    
    author='Maayane T. Soumagnac, Noam Ganot, Ido Irani, Erez Zimmerman',
    author_email='maayane.soumagnac@weizmann.ac.il',  # Optional
    keywords='astronomy',  # Optional
    packages=["SOPRANOS"],
    #packages=find_packages(),
    install_requires=['numpy','matplotlib'],  # Optional
    python_requires='>=3',
)
