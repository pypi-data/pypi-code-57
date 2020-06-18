from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="p-1",
    version="1.0.1",
    description="A Python package to get my name",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/nikhilkumarsingh/weather-reporter",
    author="Mukul Agrawal",
    author_email="agmukul63@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["p_1"],
    include_package_data=True,
    #install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "p-1=p_1.first:mukul",
        ]
    },
)