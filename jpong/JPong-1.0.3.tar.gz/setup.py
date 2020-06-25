from setuptools import setup, find_packages

version = {}

with open("./pong/version.py", "r") as fh:
    exec(fh.read(), version)

setup(
    name="JPong",
    version=version.get("__version__", "0.0.1"),
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
