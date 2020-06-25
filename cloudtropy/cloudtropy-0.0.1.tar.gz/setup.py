"""`setup.py`"""
from setuptools import setup, find_packages

# # Package requirements
# with open('requirements.txt') as f:
#     INSTALL_REQUIRES = [l.strip() for l in f.readlines() if l]

INSTALL_REQUIRES=[
'numpy',
'scikit-learn',
'scipy',
'matplotlib'
]

setup(name='cloudtropy',
      version='0.0.1',
      description='Empirical probability mass functions and entropies of N-dimensional clouds of points.',
      author='Pedro Ramaciotti Morales',
      author_email='pedro.ramaciotti@gmail.com',
      url = 'https://github.com/pedroramaciotti/Cloudtropy',
      download_url = 'https://github.com/pedroramaciotti/Cloudtropy/archive/0.0.1.tar.gz',
      keywords = ['entropy','probabilities'],
      packages=find_packages(),
      data_files=[('', ['LICENSE'])],
      install_requires=INSTALL_REQUIRES)
