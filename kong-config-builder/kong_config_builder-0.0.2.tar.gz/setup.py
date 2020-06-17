from setuptools import setup, find_packages

with open("requirements.txt") as reqs:
    requirements = reqs.read().split("\n")

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="kong_config_builder",
    version="0.0.2",
    description="Kong declarative configuration builder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Olx",
    license='MIT',
    include_package_data=True,
    url='https://github.com/olxbr/kong-config-builder/',
    download_url='https://github.com/olxbr/kong-config-builder/archive/master.zip',
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
    ],
    packages=find_packages()
)
