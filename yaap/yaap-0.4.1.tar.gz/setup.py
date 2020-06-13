from setuptools import setup

setup(
    name="yaap",
    author="Kang Min Yoo",
    author_email="kangmin.yoo@gmail.com",
    description="Yet another argument parser (Yaap)",
    url="https://github.com/kaniblu/yaap",
    keywords="argument parser config file",
    version="0.4.1",
    packages=["yaap"],
    install_requires=[
        "pyyaml==5.1.1",
        "jsonschema==3.0.1"
    ]
)
