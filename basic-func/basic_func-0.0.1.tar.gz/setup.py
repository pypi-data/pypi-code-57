from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='basic_func',
  version='0.0.1',
  description='A bunch of basic functions needed for all Python programs',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='Shanvanth Arunmozhi',
  author_email='shanvantharunmozhi@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='functions', 
  packages=find_packages(),
  install_requires=[''] 
)