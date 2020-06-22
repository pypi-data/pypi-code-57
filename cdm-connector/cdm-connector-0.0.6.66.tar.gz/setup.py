from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="cdm-connector",
    version="0.0.6.66",
    description="A Python package to read and write files in CDM format. Customized for SkyPoint use cases.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/skypointcloud/skypoint-python-cdm-connector",
    author="SkyPoint Cloud",
    author_email="support@skypointcloud.com",
    license="GPL-3.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["skypoint_python_cdm"],
    package_data={'skypoint_python_cdm':['config/*',]},
    include_package_data=True,
    install_requires=["pandas==1.0.1","azure-storage-blob==2.1.0","numpy==1.18.2", "retry==0.9.2", "boto3==1.14.2", "botocore==1.17.2"]
)