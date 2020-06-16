import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

required_packages=[
    'google-cloud-logging>=1.10.0',
    'google-cloud-datastore>=1.8.0',
    'google-cloud-bigquery>=1.16.0',
    'google-cloud-storage>=1.15.0',
    'google-cloud-kms>=1.2.1',
    'gcsfs>=0.1.2',
    'pyarrow>=0.12.1 ',
    'pandas>=0.24.1',
    'redis>=3.0.1',
    'google-auth>=1.5.0',
    'pyjwt>=1.7.1',
    'cryptography>=2.8',
    'google-cloud-secret-manager>=1.0.0'
]

setuptools.setup(
    name="mms-pip",
    version="0.8.3.0",
    author="Josef Goppold, Tobias Hoke",
    author_email="goppold@mediamarktsaturn.com, hoke@mediamarktsaturn.com",
    description="A custom MMS Analytics module for Python3 by the Data Access Team",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MediaMarktSaturn/mms-pip",
    packages=setuptools.find_packages(),
    install_requires=required_packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
