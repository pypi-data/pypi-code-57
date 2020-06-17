with open('readme.rst', 'r') as f:
    readme = f.read()
    
def parse_requirements(filename):
    ''' Load requirements from a pip requirements file '''
    with open(filename, 'r') as fd:
        lines = []
        for line in fd:
            line.strip()
            if line and not line.startswith("#"):
                lines.append(line)
    return lines

requirements = parse_requirements('requirements.txt')

#from distutils.core import setup, Extension
from setuptools import setup, Extension
from pyLIA import __version__
setup(name='pyLIA',
      version=__version__,
      author='Lorenzo Capponi',
      author_email='lorenzocapponi@outlook.it',
      description='Module for Lock-In Analysis',
      url='https://github.com/LolloCappo/pyLIA',
      py_modules=['pyLIA'],
      long_description=readme,
      install_requires=requirements
      )