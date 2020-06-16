from setuptools import setup, find_packages

setup(name='bankaya-data-utilities',
      version='0.1',
      url='https://bitbucket.org/bankaya-dev/data-utilities',
      license='Bankaya',
      author='Enrique Garcia & Ricardo Mansilla',
      author_email='enrique@bankaya.com.mx',
      description='Driver for data access utilities',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False)