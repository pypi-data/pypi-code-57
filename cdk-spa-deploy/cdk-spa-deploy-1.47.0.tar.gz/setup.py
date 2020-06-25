import json
import setuptools

kwargs = json.loads("""
{
    "name": "cdk-spa-deploy",
    "version": "1.47.0",
    "description": "This is an AWS CDK Construct to make deploying a single page website (Angular/React/Vue) to AWS S3 behind SSL/Cloudfront as easy as 5 lines of code.",
    "license": "MIT",
    "url": "https://github.com/nideveloper/CDK-SPA-Deploy.git",
    "long_description_content_type": "text/markdown",
    "author": "hello@cdkpatterns.com",
    "project_urls": {
        "Source": "https://github.com/nideveloper/CDK-SPA-Deploy.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "spa_deploy",
        "spa_deploy._jsii"
    ],
    "package_data": {
        "spa_deploy._jsii": [
            "cdk-spa-deploy@1.47.0.jsii.tgz"
        ],
        "spa_deploy": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.7.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-certificatemanager==1.47.0",
        "aws-cdk.aws-cloudfront==1.47.0",
        "aws-cdk.aws-route53-patterns==1.47.0",
        "aws-cdk.aws-route53-targets==1.47.0",
        "aws-cdk.aws-s3==1.47.0",
        "aws-cdk.aws-s3-deployment==1.47.0",
        "aws-cdk.core==1.47.0"
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
        "License :: OSI Approved"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
