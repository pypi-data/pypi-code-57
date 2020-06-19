from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="p-2",
    version="1.0.1",
    description="A Python package to get my name",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/agmukul",
    author="Abhishek",
    author_email="abhishek08arora@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["p_2"],
    include_package_data=True,
    #install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "p-2=p_2.Batch:name",
        ]
    },
)
