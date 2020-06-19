import setuptools


with open("README.rst", "r") as readme:
    long_description = readme.read()

setuptools.setup(name = "molgemtools",
                 version = "0.0.1",
                 author = "Attila Dékány",
                 author_email = "dekanyattilaadam@gmail.com",
                 description = "Tools for working with molecular geometry data.",
                 long_description = long_description,
                 url = "https://gitlab.com/d_attila/molgemtools.git",
                 packages = setuptools.find_packages(),
                 license = "MIT",
                 package_data = {"" : ["data/*",
                                       "data/alanine/*",
                                       "data/alanine/conformers/*"]},
                 classifiers = ["Programming Language :: Python :: 3",
                                "Operating System :: OS Independent"],
                 python_requires = '>=3.6',
                 setup_requires=["numpy"],
                 install_requires=["numpy"])
