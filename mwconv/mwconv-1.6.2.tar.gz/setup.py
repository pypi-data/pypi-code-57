#!/usr/bin/env python

from setuptools import setup

with open('README.md') as f:
    long_desc = f.read()

setup(name='mwconv',
      version='1.6.2',
      description='Wiki text convertions based on MediaWiki',
      long_description=long_desc,
      long_description_content_type="text/markdown",
      author='Steve Ratcliffe',
      author_email='steve@itinken.com',
      url='https://hg.sr.ht/~sratcliffe/mwconv',
      license='MIT',
      classifiers=[
          'Development Status :: 5 - Production/Stable',

          'Intended Audience :: Developers',

          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: MIT License',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          ],
      packages=['mwconv', 'mwconv.writer'],
      entry_points={
          'console_scripts': ['mwconv = mwconv:main']
      },
      install_requires=['six', 'pygments']
  )
