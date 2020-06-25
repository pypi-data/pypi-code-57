
import sys
import os


# Make sure we are running python3.5+
if 10 * sys.version_info[0] + sys.version_info[1] < 35:
    sys.exit("Sorry, only Python 3.5+ is supported.")


from setuptools import setup


def readme():
    print("Current dir = %s" % os.getcwd())
    print(os.listdir())
    with open('README.rst') as f:
        return f.read()

setup(
      name             =   'medcon',
      # for best practices make this version the same as the VERSION class variable
      # defined in your ChrisApp-derived Python class
      version          =   '1.1.0.0',
      description      =   'A ChRIS DS plugin that wraps around medcon and provides NifTI to DICOM conversion capability.',
      long_description =   readme(),
      author           =   'Arushi Vyas / Rudolph Pienaar',
      author_email     =   'dev@babyMRI.org',
      url              =   'https://github.com/FNNDSC/pl-medcon',
      packages         =   ['medcon'],
      install_requires =   ['chrisapp', 'pudb'],
      test_suite       =   'nose.collector',
      tests_require    =   ['nose'],
      scripts          =   ['medcon/medcon.py'],
      license          =   'MIT',
      zip_safe         =   False
     )
