import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thmcli",
    version="0.1.0",
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
    install_requires=[
        "argh==0.26.2",
        "thmapi==0.8.0",
        "requests",
        "chardet>=3.0.2,<4",
        "idna>=2.5,<3",
        "urllib3>=1.21.1,<1.26,!=1.25.0,!=1.25.1",
        "certifi>=2017.4.17"

    ],
    entry_points={
        'console_scripts': ['thm = thmcli.cli:main']
    },
)
