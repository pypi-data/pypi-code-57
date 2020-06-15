import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'fuelcell',
  version = '1.3.7',
  description = 'data processing for fuel cell and electrolyzer experiments',
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  url = 'https://github.com/samaygarg/fuelcell',
  author = 'Samay Garg',
  author_email = 'samay.garg@berkeley.edu',
  license = 'MIT',
  classifiers=[
    'Development Status :: 4 - Beta',
    'Programming Language :: Python :: 3'
  ],
  keywords = ['tintin', 'snowy', 'haddock', 'fuelcell'],
  packages=setuptools.find_packages(),
  python_requires='>=3',
  install_requires=['numpy', 'pandas', 'matplotlib', 'PySide2'],
  project_urls={
    'Documentation': 'https://fuelcell.readthedocs.io/en/latest/',
    'Source': 'https://github.com/samaygarg/fuelcell'
  }
)