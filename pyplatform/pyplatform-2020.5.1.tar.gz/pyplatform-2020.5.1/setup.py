from setuptools import setup, find_namespace_packages
import re
import os
import sys
import codecs

# with open('requirements.txt') as f:
#     required = f.read().splitlines()

try:
    # https://stackoverflow.com/questions/30700166/python-open-file-error
    with codecs.open("README.md", 'r', errors='ignore') as file:
        readme_contents = file.read()

except Exception as error:
    readme_contents = ""
    sys.stderr.write("Warning: Could not open README.md due %s\n" % error)


setup(name='pyplatform',
      version='2020.5.1',
      description='Pyplatform is a data analytics platform architeture built around Google BigQuery in a hybrid cloud environment.',
      long_description=readme_contents,
      long_description_content_type="text/markdown",
      url='https://github.com/mhadi813/pyplatform',
      author='Muhammad Hadi',
      author_email='mhadi813@gmail.com',
      license='BSD',
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "Topic :: Office/Business",
          "License :: OSI Approved :: BSD License",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
      ],
      install_requires=['pyplatform-datawarehouse','pyplatform-database','pyplatform-datalake','pyplatform-reporting'],
      keywords="google bigquery cloud functions storage jupyterlab python SQL",
      zip_safe=False)
