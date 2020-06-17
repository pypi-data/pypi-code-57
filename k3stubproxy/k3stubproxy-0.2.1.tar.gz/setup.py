from setuptools import setup, find_packages
import re

def get_version():
    with open("k3stubproxy/_version.py") as fh:
        verLine = fh.read()
        m = re.match("\s*__version__ *= *[\"']([\d.]+)[\"']", verLine)
        if m:
            return m.group(1)
        else:
            raise RuntimeError("Unable to determine version of the project")

def get_long_description():
    with open("README.md", "r") as fh:
        return fh.read()


setup(
    name='k3stubproxy',
    version=get_version(),
    
    # project description parameters. These should be filled in accordingly
    author="Joachim Kestner",
    author_email="joachim.kestner@khoch3.de",
    description="A library that simplifies proxying stub functions in c",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    python_requires='~=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    
    # packages for distribution are found & included automatically
    packages=find_packages(),
    # for defining other resource files if they need to be included in the installation
    package_data={
        '' : ['*.md']
    },
    
    # Set this is using a MANIFEST.in 
    # include_package_data=True,
    
    # libraries from PyPI that this project depends on
    install_requires=[
        # example library
        "k3logging==0.1",
        "k3process==0.4"
    ],
    entry_points={
        'console_scripts': [
            # a list of strings of format:
            # <command> = <package>:<function>
            'k3stubproxy-generate-stub = k3stubproxy.main.stubgenerator:main',
            'k3stubproxy-analyse-stub-function-definition = k3stubproxy.main.dump_function_definition:main',
            'k3stubproxy-generate-target-stub = k3stubproxy.main.stub_target_generator:main'
            # , ...
        ]
    }
)