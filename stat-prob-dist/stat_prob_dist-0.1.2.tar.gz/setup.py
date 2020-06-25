from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name = 'stat_prob_dist',
      version = '0.1.2',
      description = 'Statistical distributions - Gaussian, Binomial etc..',
      packages = ['stat_prob_dist'],
      author = 'Amanpreet Singh',
      author_email = 'amanpreetsingh459@gmail.com',
      zip_safe = False)
