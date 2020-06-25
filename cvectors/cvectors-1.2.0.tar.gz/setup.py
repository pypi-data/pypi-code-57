import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="cvectors",
    version="1.2.0",
    author="Tom Fryers",
    description="A simple complex vector package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Tom_Fryers/cvectors",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
