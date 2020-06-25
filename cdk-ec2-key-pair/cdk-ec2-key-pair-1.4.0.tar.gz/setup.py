import json
import setuptools

kwargs = json.loads("""
{
    "name": "cdk-ec2-key-pair",
    "version": "1.4.0",
    "description": "CDK Construct for managing EC2 key pairs",
    "license": "Apache-2.0",
    "url": "https://github.com/udondan/cdk-ec2-key-pair",
    "long_description_content_type": "text/markdown",
    "author": "Daniel Schroeder",
    "project_urls": {
        "Source": "https://github.com/udondan/cdk-ec2-key-pair.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_ec2_key_pair",
        "cdk_ec2_key_pair._jsii"
    ],
    "package_data": {
        "cdk_ec2_key_pair._jsii": [
            "cdk-ec2-key-pair@1.4.0.jsii.tgz"
        ],
        "cdk_ec2_key_pair": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.7.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-cloudformation>=1.47.0, <2.0.0",
        "aws-cdk.aws-iam>=1.47.0, <2.0.0",
        "aws-cdk.aws-kms>=1.47.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.47.0, <2.0.0",
        "aws-cdk.core>=1.47.0, <2.0.0",
        "constructs>=3.0.4, <4.0.0",
        "iam-floyd>=0.13.0, <0.14.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
