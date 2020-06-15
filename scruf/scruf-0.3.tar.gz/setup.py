import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    author="Matthew Hughes",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Testing",
    ],
    description="Functional testing for command line applications",
    license="GNU GPLv3",
    long_description=long_description,
    name="scruf",
    packages=["scruf", "scruf.observers"],
    python_requires=">=3.6",
    scripts=["bin/scruf"],
    url="https://gitlab.com/matthewhughes/scruf",
    version="0.3",
)
