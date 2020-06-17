import sys
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
  os.system('python setup.py sdist bdist_wheel')
  os.system('twine upload dist/*')
  sys.exit()

# 'setup.py pre-publish' shortcut.
if sys.argv[-1] == 'pre-publish':
  os.system('python setup.py sdist bdist_wheel')
  os.system('twine upload --repository testpypi dist/*')
  sys.exit()

packages = ['mapper', 'mapper.*']

requires = [
  'importlib-metadata==1.6.1',
  'nltk==3.5',
  'unidecode==1.1.1',
  'requests==2.23.0'
]

about = {}
with open(os.path.join(here, 'mapper', '__version__.py'), 'r', encoding='utf8') as f:
  exec(f.read(), about)

with open("README.md", "r") as fh:
  readme = fh.read()

setup(
  name=about['__title__'],
  version=about['__version__'],
  description=about['__description__'],
  long_description=readme,
  long_description_content_type="text/markdown",
  author=about['__author__'],
  author_email=about['__author_email__'],
  url=about['__url__'],
  packages=find_packages(include=packages),
  python_requires='>=3.7',
  install_requires=requires,
  license=about['__license__'],
  classifiers=[
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    "Operating System :: OS Independent",
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
  entry_points = {
    'console_scripts': ['setup-nltk=setup_nltk:install_nltk_data']
  },
  keywords = ['auto', 'mapper', 'mapping', 'text processing', 'text similarity'],
)