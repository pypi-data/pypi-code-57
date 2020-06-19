from os import makedirs, system, getcwd
from os.path import isdir, isfile
from loguru import logger as log


class Project(object):
    @classmethod
    def get_current_project_name(cls):
        return getcwd().split("/")[-1]

    @classmethod
    def compile(cls):
        if isfile("setup.py"):
            log.debug("compiling '{0}'".format(cls.get_current_project_name()))
            system("python3 setup.py bdist sdist")

    @classmethod
    def upload(cls):
        if isdir("dist"):
            log.debug("uploading '{0}' to pypi".format(cls.get_current_project_name()))
            system("twine upload dist/*")

    @classmethod
    def touch(cls, fp):
        log.debug("creating file '{0}'".format(fp))
        system("touch {0}".format(fp))

    @classmethod
    def write(cls, fp, data):
        log.debug("writing data to '{0}'".format(fp))
        with open(fp, "w") as f:
            f.write(data)

    @classmethod
    def new(cls, name, mit, author):
        log.info("creating project '{0}'".format(name))
        pd = "{0}/{0}".format(name)

        if not isdir(pd):
            makedirs(pd)
        else:
            log.exception("the project '{0}' already exists.".format(name))
            exit()
        cls.write("{0}/README.md".format(name), "## {0}".format(name))
        cls.touch("{0}/requirements.txt".format(name))
        cls.touch("{0}/__init__.py".format(pd))

        cls.write("{0}/__main__.py".format(pd), """from argparse import ArgumentParser


def main():
    ap = ArgumentParser()

    a = ap.parse_args()


if __name__ == '__main__':
    main()
""")

        cls.write("{0}/setup.py".format(name), """from setuptools import setup, find_packages

setup(
    long_description_content_type="text/markdown",
    long_description=open("README.md", "r").read(),
    name="{0}",
    version="0.1",
    # description="",
    # author="",
    # author_email="",
    # url="",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    # keywords="",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            '{0} = {0}.__main__:main'
        ]
    },
    install_requires=open("requirements.txt").readlines()
)
""".replace("{0}", name))

        if mit:
            cls.write("{0}/LICENSE".format(name), """The MIT License

Copyright (c) 2019 {0}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
""".format(author))
