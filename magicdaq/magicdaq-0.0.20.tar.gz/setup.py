# This is an example packaging:
# https://packaging.python.org/tutorials/packaging-projects/

# How to include extra files
# MANIFEST.in: https://medium.com/@thucnc/how-to-publish-your-own-python-package-to-pypi-4318868210f9

# OLD NOTES:
# This is how you install wheel:
# python32 -m pip install --user --upgrade setuptools wheel

#*** Build a new wheel: ***
# python32 setup.py sdist bdist_wheel

# Package extra files with MANIFEST.IN
# https://medium.com/@thucnc/how-to-publish-your-own-python-package-to-pypi-4318868210f9

# Get twine:
# python32 -m pip install --user --upgrade twine

#*** Upload via twine: ***
# python32 -m twine upload dist/*
# Upload to the testpypi
# python32 -m twine upload --repository testpypi dist/*

# Uploaded to:
# https://test.pypi.org/project/hellopypicrug/1.0/


# Notes on using test pypi:
# https://packaging.python.org/guides/using-testpypi/
# Download from pypi:
# python32 -m pip install -i https://test.pypi.org/simple/ hellopypicrug==1.0

#*** Download Update ***
# python32 -m pip install -i https://test.pypi.org/simple/ example-pkg-Trendeca --upgrade
# Need to run the below command twice
# python32 -m pip install -i https://test.pypi.org/simple/ magicdaq --upgrade

# Simple Tutorial
# https://packaging.python.org/tutorials/packaging-projects/

# Instructions on how to do PyPi:
# https://towardsdatascience.com/writing-a-python-package-561146e53351

# Build and install wheel file locally:
# python -m pip install .

# How to find install path:
# >>> import sys
# >>> for path in sys.path:
# ...     print(path)

#These are the import paths for python
# For 64 Bit Python on this computer:
# C:\Users\dcba\AppData\Local\Programs\Python\Python37\python37.zip
# C:\Users\dcba\AppData\Local\Programs\Python\Python37\DLLs
# C:\Users\dcba\AppData\Local\Programs\Python\Python37\lib
# C:\Users\dcba\AppData\Local\Programs\Python\Python37
# C:\Users\dcba\AppData\Local\Programs\Python\Python37\lib\site-packages

# For 32 Bit Python on this computer:
# C:\Python3,32bit\python37.zip
# C:\Python3,32bit\DLLs
# C:\Python3,32bit\lib
# C:\Python3,32bit
# C:\Users\dcba\AppData\Roaming\Python\Python37\site-packages
# C:\Python3,32bit\lib\site-packages


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="magicdaq", # Replace with your own username
    version="0.0.20",
    author="MagicDAQ Support",
    author_email="support@magicdaq.com",
    description="Python API for MagicDAQ Data Acquisition and Test Automation Device",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.magicdaq.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows ",
    ],
    python_requires='>=3.0',
    include_package_data = True,
)
