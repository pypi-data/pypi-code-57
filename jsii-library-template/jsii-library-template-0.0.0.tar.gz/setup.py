import json
import setuptools

kwargs = json.loads("""
{
    "name": "jsii-library-template",
    "version": "0.0.0",
    "description": "Template for jsii libraries",
    "license": "Apache-2.0",
    "url": "https://github.com/eladb/jsii-library-template.git",
    "long_description_content_type": "text/markdown",
    "author": "Elad Ben-Israel<benisrae@amazon.com>",
    "project_urls": {
        "Source": "https://github.com/eladb/jsii-library-template.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "jsii_library_template",
        "jsii_library_template._jsii"
    ],
    "package_data": {
        "jsii_library_template._jsii": [
            "jsii-library-template@0.0.0.jsii.tgz"
        ],
        "jsii_library_template": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.5.0, <2.0.0",
        "publication>=0.0.3"
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
