import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-robotics", # Replace with your own username
    version="0.0.1",
    author="Adwait Naik",
    author_email="adwaitnaik2@gmail.com.com",
    description="Implementation of path planning algorithms in python.",
    long_description="a collection of path planning algorithms implemented using python.",
    long_description_content_type="text/markdown",
    url="https://github.com/addy1997/py-robotics",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
