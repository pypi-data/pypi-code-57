# -*- coding: utf-8 -*-
"""
@author: Suhas Sharma and Rahul P
"""

from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["beautifulsoup4>=4.9.0", "bs4>=0.0.1", "numpy>=1.18.2", "pandas>=1.0.4", "python-whois>=0.7.2", "requests>=2.23.0", "scikit-learn>=0.21.3", "selenium>=3.141.0", "sklearn>=0.0", "tqdm>=4.46.0", "urllib3>=1.25.8"]

setup(
      name="fluffypancakes",
      version="0.1.2",
      description="Detect Phishing Websites using Machine Learning",
      author="Suhas Sharma",
      author_email="le.bon.garconn@gmail.com",
      long_description=readme,
      long_description_content_type="text/markdown",
      url="https://github.com/suhasrsharma/FluffyPancakes",
      #py_modules=["fluffypancakes", "features", "handler", "recurrent"],
      py_modules=["__init__"],
      #package_dir={'': 'fluffypancakes'},
      packages=find_packages(),
      keywords="web-phishing-detection machine-learning",
      include_package_data=True,
      install_requires=requirements,
      extras_require={
              "dev":[
                      "pytest>=3.7",
                      "twine>=3.1.1"
                      ]
                  },
      classifiers=[
              "Development Status :: 4 - Beta",
              "Intended Audience :: Developers",
              "Intended Audience :: Education",
              "License :: OSI Approved :: MIT License",
              "Operating System :: OS Independent",
              "Programming Language :: Python :: 2.7",
              "Programming Language :: Python :: 3",
              "Programming Language :: Python :: 3.6",
              "Programming Language :: Python :: 3.7"
              ]
      )