import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thmcli",
    version="0.0.1",
    author="Szymon Borecki",
    author_email="self@szymex.pw",
    description="TryHackMe CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/szymex73/thmcli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha"
    ],
    python_requires='>=3.8',
)
