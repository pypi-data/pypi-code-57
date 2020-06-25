import setuptools

__version__ = "1.2.4"

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="ems-dataflow-testframework",
    version=__version__,
    author="Emarsys",
    description="Framework helping testing Google Cloud Dataflows",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["tests", "test_.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "atomicwrites==1.3.0",
        "attrs==19.1.0",
        "cachetools==3.1.1",
        "certifi==2019.6.16",
        "chardet==3.0.4",
        "ems-gcp-toolkit==0.1.73",
        "google-auth==1.6.3",
        "google-cloud-bigtable==1.0.0",
        "google-resumable-media==0.4.0",
        "grpcio==1.23.0",
        "idna==2.8",
        "importlib-metadata==0.21",
        "inflection==0.3.1",
        "more-itertools==7.2.0",
        "packaging==19.1",
        "pluggy==0.13.0",
        "protobuf==3.9.1",
        "py==1.8.0",
        "pyasn1==0.4.7",
        "pyasn1-modules==0.2.6",
        "pyparsing==2.4.2",
        "pytest==5.1.2",
        "pytz==2019.2",
        "requests==2.22.0",
        "rsa==4.0",
        "six==1.12.0",
        "tenacity==5.1.1",
        "urllib3==1.25.3",
        "wcwidth==0.1.7",
        "zipp==0.6.0"
    ]
)
