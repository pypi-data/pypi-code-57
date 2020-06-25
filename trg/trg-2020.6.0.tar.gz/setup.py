import codecs
import os
import re

from setuptools import find_packages, setup


def open_local(paths, mode="r", encoding="utf8"):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), *paths)
    return codecs.open(path, mode, encoding)


def get_version(*args):
    with open_local(args, encoding="latin1") as fp:
        try:
            version = re.findall(
                r"^__version__ = \"([\d\.]+)\"\r?$", fp.read(), re.M
            )[0]
            return version
        except IndexError:
            raise RuntimeError("Unable to determine version.")


def get_requirements(*args):
    requirements = []
    with open_local(args, encoding="latin1") as fp:
        for ln in fp:
            if ln.startswith("#"):
                continue
            if ln.find("==") > -1:
                # requirements found, let's check if there's any comments
                if ln.find("#") > -1:
                    # we need to check if this comes from requirements or not
                    dep, annotation = ln.split("#")
                    if annotation.find("via -r requirements.in") > -1:
                        pkg = dep
                    else:
                        # dependency of a dependency
                        continue
                pkg = ln.strip()  # clean up any whitespace in there
                pkg = pkg.split("==")[0]
                if pkg not in requirements:
                    requirements.append(pkg)
    return requirements


version = get_version("src", "trg", "__init__.py")
long_description = ""

with open_local(["README.rst"]) as fp:
    long_description += fp.read()
    long_description += "\n"

with open_local(["CHANGELOG.rst"]) as fp:
    long_description += fp.read()

setup(
    name="trg",
    version=version,
    license="MIT license",
    description="To do a better description",
    long_description=long_description,
    author="Richard Kuesters",
    author_email="rkuesters@gmail.com",
    url="https://github.com/vltr/trg",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        # "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Utilities",
    ],
    keywords=[],
    install_requires=get_requirements("requirements.txt"),
    extras_require={},
    tests_require=[],
)
