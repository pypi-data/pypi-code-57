from setuptools import setup, find_packages


setup(
    name="uenginecli",
    version="1.0.2",
    description="a helper client library for accessing uengine-based APIs",
    url="https://github.com/viert/uenginecli",
    author="Pavel Vorobyov",
    author_email="aquavitale@yandex.ru",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "requests",
    ]
)
