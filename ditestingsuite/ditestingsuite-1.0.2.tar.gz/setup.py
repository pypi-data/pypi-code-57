from setuptools import setup

setup(name='ditestingsuite',
      version='1.0.2',
      author='Tong Wang',
      author_email='tong.wang@di.net.au',
      license='MIT',
      packages=['ditestingsuite'],
      install_requires=['atlassian-python-api','PyYAML'],
      zip_safe=False)