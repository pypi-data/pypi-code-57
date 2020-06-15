import sys
import os
from setuptools import setup, find_packages

req_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "requirements.txt")
with open(req_path) as f:
    reqs = f.read().splitlines()


setup(name="maxar-skyway",
      version="0.0.2",
      author="Jamison Polackwich",
      author_email='jamie.polackwich@digitalglobe.com',
      description="Python API for making OSM queries",
      url="https://github.com/maxar-analytics/skyway",
      license="MIT",
      packages=find_packages(exclude=['docs', 'tests']),
      install_requires=reqs,
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License"
    ],
      python_requires='>3.7',
      )

