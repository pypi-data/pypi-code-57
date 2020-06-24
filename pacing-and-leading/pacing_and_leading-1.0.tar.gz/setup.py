from setuptools import setup,find_packages
import sys
from os import path

with open(path.join(path.dirname(__file__), 'VERSION')) as v:
        VERSION = v.readline().strip()
        
setup(name = "pacing_and_leading",
      packages=find_packages('.'),
      version = VERSION,
      description="pacing and leading experiment",
      author="Vincent Berenz",
      author_email="vberenz@tuebingen.mpg.de",
      scripts=['bin/pacing_and_leading',
               'bin/pacing_and_leading_simlog'],
      install_requires = ["matplotlib","numpy"])

