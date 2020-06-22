from setuptools import setup, find_packages

setup(name='eft',
      description='A efficient finance tool for personal usage',
      version='0.0.7',
      author='jarvixwang',
      packages=find_packages(),
      package_dir={'eft': 'eft'},
      package_data={'eft': ['*.*']},
      install_requires=open('requirements.txt').read().splitlines(),
      )
