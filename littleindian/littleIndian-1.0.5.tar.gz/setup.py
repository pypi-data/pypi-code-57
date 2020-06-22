from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="littleIndian",
    version="1.0.5",
    description="A demo package to print the lyrics of the Little Indian song",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/pythoslabs/littleIndian",
    author="Pythos Labs",
    author_email="pythoslabs@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["littleIndian"],
    include_package_data=True,
)






