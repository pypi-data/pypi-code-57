from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='terminal-fun',    # Module Name
    version='0.0.1',
    description='Various Fun Terminal Commands!',
    py_modules=["terminalfun"],      # Py File Name in src
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ], 
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = [
        "cowsay>=2.0.3",
    ],
    extras_require = {
        "dev": [
            "pytest==5.4.3",
        ],
    },
    url="https://github.com/himanshujain171/terminal-fun",
    author="Himanshu Jain",
    author_email="nhimanshujain@gmail.com", 

) 