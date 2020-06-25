import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="evolutiongaming-bundle-downloader",
    version="1.0",
    author="Ozgur Vatansever",
    author_email="ozgurvt@gmail.com",
    description="Downloads all available games from the bundle repository.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bundle-repo.evo-games.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=2.7",
    install_requires=["requests"]
)
