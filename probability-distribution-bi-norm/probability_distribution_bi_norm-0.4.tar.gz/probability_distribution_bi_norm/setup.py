from setuptools import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='probability_distribution_bi_norm',
      version='0.4',
      description='Gaussian and Binomial distributions',
      packages=['probability_distribution_bi_norm'],
      author="Zainab Ayodimeji",
      author_email ="zayodimeji@gmail.com",
      zip_safe=False)
