# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.md','r',encoding='utf-8-sig') as f:
    long_description = f.read()

requirements = [
    'ntplib'
]

setup(name='ntptimenow',
      version='0.4',
      description='Python NTP Time Now',
      author='Wannaphong Phatthiyaphaibun',
      author_email='wannaphong@kkumail.com',
      url='https://github.com/wannaphong/pyntptimenow',
      py_modules=['ntptimenow'],
      install_requires = requirements,
      license='MIT',
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Operating System :: OS Independent',
          'Topic :: System :: Networking :: Time Synchronization'
      ],
      long_description=long_description,
      long_description_content_type = "text/markdown",
     )