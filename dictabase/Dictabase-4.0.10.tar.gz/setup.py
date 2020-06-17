from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

packages = ['dictabase']
print('packages=', packages)

setup(
    name="Dictabase",

    version="4.0.10",
    # 4.0.10 Updated Readme with RegisterDBURI()
    # 4.0.9 Bug fix in FindAll()
    # 4.0.8 Cleaned up debug prints
    # 4.0.7 Bug fix in BaseTable.__del__()
    # 4.0.6 Bug fix when FindOne() returns None
    # 4.0.5 Bug fix with Overlapping references in FindOne() and FindAll()
    # 4.0.4 Used threading.Lock instead of while loop
    # 4.0.3 Added check_same_thread for sqlite dbs
    # 4.0.2 Added SetDebug feature to enable/disable debug on the fly
    # 4.0.1 fixed import error
    # 4.0.0 refactored package into multiple sub-modules, made single-threaded within the package, but thread-safe outside
    # 3.0.6 prevent race conditins in Drop(), Delete(), New()
    # 3.0.5 prevent race conditions in FindAll() and FindOne()
    # 3.0.4 restructured BaseTable to use methods BaseTable.DumpKey() and BaseTable.LoadKey()
    # 2.3.0 refactored BaseTable into two classes
    # 2.2.2 refactored BaseTable with getter/setter wrappers
    # 2.1.1 bug fix when defining json-able kwargs in New()
    # 2.1.0 can now store json-able types
    # 2.0.0 optimized it all
    # 1.3.2 fixed unnecessary connections to db
    # 1.3.1 optimized
    # 1.3.0 protected against race/conditions in multi-threaded system
    # 1.2.6 added relational mapping
    # 1.2.5 changed README to rst
    # 1.2.4 updated README
    # 1.2.3 added dependencies
    # 1.2.2 changed from module to package
    # 1.2.1 updated readme
    # 1.1 updated readme

    packages=packages,
    install_requires=['dataset'],
    # scripts=['say_hello.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    # install_requires=['docutils>=0.3'],

    # package_data={
    #     # If any package contains *.txt or *.rst files, include them:
    #     '': ['*.txt', '*.rst'],
    #     # And include any *.msg files found in the 'hello' package, too:
    #     'hello': ['*.msg'],
    # },

    # metadata to display on PyPI
    author="Grant miller",
    author_email="grant@grant-miller.com",
    description="A database interface that mimics a python dictionary.",
    long_description=long_description,
    license="PSF",
    keywords="dictionary database dictabase grant miller sqlalchemy flask sqlite dataset",
    url="https://github.com/GrantGMiller/dictabase",  # project home page, if any
    project_urls={
        "Source Code": "https://github.com/GrantGMiller/dictabase",
    }

    # could also include long_description, download_url, classifiers, etc.
)

# to push to PyPI

# test postgres: 'postgres://xfgkxpzruxledr:5b83aece4fbad7827cb1d9df48bf5b9c9ad2b33538662308a9ef1d8701bfda4b@ec2-35-174-88-65.compute-1.amazonaws.com:5432/d8832su8tgbh82'
# python -m setup.py sdist bdist_wheel
# twine upload dist/*