from setuptools import setup
def get_read_me():
    with open("README.md", "r") as fh:
        long_description = fh.read()
    return long_description


setup(
    author='AmirBahadorDev',
    author_email='amirbahadordev@gmail.com',
    url='https://github.com/AmirBahadorDev/elk-stack.git',
    name='elk-stack',
    version='0.0.1',
    description='Complete ElasticSearch Stack',
    py_modules=["elk"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 7 - Inactive",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=get_read_me(),
    long_description_content_type="text/markdown",
    install_requires=[
        "requests==2.23.0",
    ],
    extras_require={
        "dev": [
            "pytest>=3.7",
        ],
    },
)
