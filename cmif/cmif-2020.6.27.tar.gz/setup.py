import os
import setuptools

ROOT = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(ROOT, 'README.rst')).read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="cmif",
    version="2020.6.27",
    author="Donatus Herre",
    author_email="pypi@herre.io",
    license="MIT",
    description="Handle data in CMI-format.",
    long_description=README,
    url="https://github.com/herreio/cmif",
    packages=setuptools.find_packages(exclude=("test",)),
    include_package_data=True,
    install_requires=required,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
)
