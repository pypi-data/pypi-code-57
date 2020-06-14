import setuptools
 
with open("README.md", "r") as fh:
  long_description = fh.read()
 
setuptools.setup(
  name = "py_mob",
  version = "0.2.5",
  author = "WenSui Liu",
  author_email = "liuwensui@gmail.com",
  description = "Python Implementation of Monotonic Optimal Binning",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  url = "https://github.com/statcompute/py_mob",
  packages = setuptools.find_packages(),
  classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)
