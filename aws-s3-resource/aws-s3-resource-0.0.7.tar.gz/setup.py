import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aws-s3-resource",
    version="0.0.7",
    author="Quaking Aspen",
    author_email="info@quakingaspen.net",
    license='MIT',
    description="This library is to ease the operations done on AWS S3 buckets and objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Quakingaspen-codehub/aws_s3_resource",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    platform=['Any'],
    python_requires='>=3.6',
    install_requires=['boto3']
)
