
from setuptools import *

with open("README.md", "r") as fh:
    long_description = fh.read()

my_packages=find_packages()


setup(
  name = 'bitsbehumble',         # How you named your package folder (MyLib)
  packages = my_packages,   # Chose the same as "name"
  version = '0.3',      # Start with a small number and increase it with every change you make      # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  long_description=long_description,

  long_description_content_type="text/markdown",  # Give a short description about your library
  author = 'Alya Gomaa',  
  url = 'https://github.com/AlyaGomaa/bitsbehumble',   # Provide either the link to your github or to your website
    # I explain this later on
  keywords = ['CTF', 'Converter'],   # Keywords that define your package best
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    
  ],
)
