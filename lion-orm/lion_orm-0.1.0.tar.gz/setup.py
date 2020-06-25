from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name="lion_orm",
    version="0.1.0",
    author="Evgeniy Blinov",
    author_email="zheni-b@yandex.ru",
    description="Lion ORM - революционная в своей примитивности ОРМ для Sqlite.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/pomponchik/lion_orm",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
