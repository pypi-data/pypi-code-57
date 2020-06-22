from setuptools import setup, find_packages
from os import path

this_dir = path.abspath(path.dirname(__file__))
with open(path.join(this_dir, "README.rst"), encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    version="1.0.2",
    name="Pomodoropie",
    description="A Python pomodoro clock",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Jeff Moorhead",
    author_email="jeff.moorhead1@gmail.com",
    url="https://github.com/Jeff-Moorhead/pomodoropie",
    packages=find_packages(),
    entry_points={"console_scripts": ["pomodoropie=pomodoropie.__main__:main"],},
)
