import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="boxwine", # Replace with your own username
    version="0.0.1",
    author="Rishabh Moudgil",
    author_email="me@rishabhmoudgil.com",
    description="Turn your Wine apps into Mac apps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rishabh/boxwine",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2',
)