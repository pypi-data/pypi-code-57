from setuptools import setup, find_packages
from pong import __version__

setup(
    name="JPong",
    version=__version__,
    description="A simple Pong game written with Pygame",
    long_description="A simple Pong game written with Pygame. The J stands for Jeff.",
    packages=find_packages(),
    author="Jeff Moorhead",
    author_email="Jeff.Moorhead1@gmail.com",
    entry_points = {
        "gui_scripts": [
            "jpong=pong.pong:main"
            ]
        },
    install_requires=["pygame"],
)
