from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="ComputerCommands",
    version="2.0.9",
    description="A Python package for running commands on any operating system.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Malacai4/ComputerCommands",
    author="Malacai Hiebert",
    author_email="malacaihiebert@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=['ComputerCommands'],
    include_package_data=True,
)
