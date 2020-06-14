from setuptools import setup, find_packages

setup(name='daproli',
      version='0.15',
      url='https://github.com/ermshaua/daproli',
      license='BSD 3-Clause License',
      author='Arik Ermshaus',
      author_email='arik@tutanota.de',
      description='daproli is a small data processing library that attempts to make data transformation more declarative.',
      packages=find_packages(exclude=['tests', 'examples']),
      install_requires=['numpy', 'joblib', 'tqdm'],
      long_description=open('README.md').read(),
      long_description_content_type="text/markdown",
      zip_safe=False)
