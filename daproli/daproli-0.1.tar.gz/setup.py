from setuptools import setup, find_packages

setup(name='daproli',
      version='0.1',
      url='https://github.com/ermshaua/daproli',
      license='BSD 3-Clause License',
      author='Arik Ermshaus',
      author_email='arik@tutanota.de',
      description='The Data Processing Library (daproli) attempts to make data manipulation more declarative and beautiful.',
      packages=find_packages(exclude=['test', 'example']),
      long_description=open('README.md').read(),
      zip_safe=False)