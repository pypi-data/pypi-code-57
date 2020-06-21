import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read().split("\n")
    requirements = [r for r in requirements if r != "" ]

setuptools.setup(
    name="sample_data", # Replace with your own username
    version="0.0.7",
    author="Joel Horowitz",
    author_email="joelhoro@gmail.com",
    description="A few sample datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joelhoro/sample_data",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
