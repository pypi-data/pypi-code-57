from setuptools import setup, find_packages

setup(
    name="JPong",
    description="A simple Pong game written with Pygame",
    packages=find_packages(),
    author="Jeff Moorhead",
    author_email="Jeff.Moorhead1@gmail.com",
    entry_points = {
        "console_scripts": [
            "jpong=pong.pong:main"
            ]
        }
)
