#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import setuptools

import buildinit

with open("README.md", "r") as fh:
    long_description = fh.read()

def get_detail(ItemName:str):
    with open("gitlab_management/__init__.py") as f:
        for line in f:
            if line.startswith("__" + ItemName + "__"):
                return(str(line.split("=")[-1]).replace('"', '').replace("\n", '').replace(" ", ''))
 
setuptools.setup(
    name=get_detail('title'), 
    version=get_detail('version'),
    author=get_detail('author'),
    author_email=get_detail('email'),
    description="GitLab group configuration as code",
    license=get_detail('licence'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/nofusscomputing/projects/python-gitlab-management",
    project_urls = {
        "Bug Tracker": "https://gitlab.com/nofusscomputing/projects/python-gitlab-management/-/issues",
        "Documentation": "https://python-gitlab-management.readthedocs.io/",
        "Source Code": get_detail('source')
    },
    packages=setuptools.find_packages(),
    install_requires=[
          'GitPython==3.1.3',
          'python-gitlab==2.2.0',
          'PyYAML==5.3.1'
    ],
    entry_points = {
        'console_scripts': ['gitlab-management=gitlab_management.cli:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)