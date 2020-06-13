from setuptools import setup

setup(
    name="yaap",
    author="Kang Min Yoo",
    author_email="kangmin.yoo@gmail.com",
    description="Yet another argument parser (Yaap)",
    url="https://github.com/kaniblu/yaap",
    keywords="argument parser config file",
    version="0.4",
    packages=["yaap"],
    install_requires=list(s.rstrip("\n") for s in open("requirements.txt", "r"))
)
