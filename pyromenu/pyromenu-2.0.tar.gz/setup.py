from setuptools import setup


def README():
    with open("README.md") as file:
        return file.read()


def requirements():
    with open("requirements.txt") as file:
        return file.read().split("\n")


setup(
    name="pyromenu",
    version="2.0",
    author="LidaRandom",
    author_email="bahoralievdev@yandex.com",
    description="Object-oriented way to build telegram keyboard-menus",
    long_description=README(),
    long_description_content_type="text/markdown",
    url="https://github.com/IlhomBahoraliev/pyromenu",
    packages=["pyromenu", "pyromenu.abc"],
    install_requires=requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
