import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dell-projector", # Replace with your own username
    version="0.0.1",
    author="Abhinav Rajaseshan",
    author_email="abhinavrajaseshan@gmail.com",
    description="A utility to control dell projectors and query their status",
    long_description="This utility querys the status and lamp life of dell projectors and also gives you basic power control of dell projectors",
    long_description_content_type="text/markdown",
    url="https://github.com/abhiseshan/dell-projector",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)