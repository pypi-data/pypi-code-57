from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="fountains",
    version="0.2.0",
    packages=["fountains",],
    install_requires=["bitlist",],
    license="MIT",
    url="https://github.com/reity/fountains",
    author="Andrei Lapets",
    author_email="a@lapets.io",
    description="Python library for generating and embedding in a compact"+\
                "way random but reproducible data for unit testing.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    test_suite="nose.collector",
    tests_require=["nose"],
)
