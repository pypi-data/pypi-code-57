import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="raenonx-toolbox",
    version="0.0.1",
    author="RaenonX JELLYCAT",
    author_email="raenonx0710@gmail.com",
    description="Personal python developing toolbox.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RaenonX/PyToolbox",
    license="MIT",
    packages=setuptools.find_packages(exclude=("tests",)),
    install_requires=["pymongo"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities"
    ],
    python_requires='>=3.6',
)
