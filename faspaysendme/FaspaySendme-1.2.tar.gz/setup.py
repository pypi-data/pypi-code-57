from setuptools import setup, find_packages

setup(name='FaspaySendme',
      version='1.2',
      url='https://github.com/faspay-team/faspay-sendme-python',
      license='MIT',
      author='Vincentius Setyo K',
      author_email='vincentius.setyo@faspay.co.id',
      description='This package provides Faspay SendMe 1.2 support for the Python Language.',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      long_description_content_type="text/markdown",
      zip_safe=False)