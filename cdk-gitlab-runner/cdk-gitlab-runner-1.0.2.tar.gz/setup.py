import json
import setuptools

kwargs = json.loads("""
{
    "name": "cdk-gitlab-runner",
    "version": "1.0.2",
    "description": "A  Gitlab Runner JSII construct lib for AWS CDK",
    "license": "Apache-2.0",
    "url": "https://github.com/guan840912/cdk-gitlab-runner.git",
    "long_description_content_type": "text/markdown",
    "author": "Neil Guan <guan840912@gmail.com>",
    "project_urls": {
        "Source": "https://github.com/guan840912/cdk-gitlab-runner.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_gitlab_runner",
        "cdk_gitlab_runner._jsii"
    ],
    "package_data": {
        "cdk_gitlab_runner._jsii": [
            "cdk-gitlab-runner@1.0.2.jsii.tgz"
        ],
        "cdk_gitlab_runner": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.6.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-ec2>=1.46.0, <2.0.0",
        "aws-cdk.aws-iam>=1.46.0, <2.0.0",
        "aws-cdk.core>=1.46.0, <2.0.0",
        "constructs>=3.0.3, <4.0.0"
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
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
