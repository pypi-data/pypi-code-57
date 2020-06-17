from setuptools import setup

with open("README.md" ,"r") as fh:
    long_desc = fh.read()


setup(
    name='helloworld_mj',
    version='0.0.1',
    description='Say Hello!',
    py_modules=["hello"],
    install_requires=[],
    extras_require = { 
        "dev": [ 
            "pytest>=3.7",
        ],
    },
    package_dir={'':'src'},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    long_description=long_desc,
    long_description_content_type="text/markdown",
)