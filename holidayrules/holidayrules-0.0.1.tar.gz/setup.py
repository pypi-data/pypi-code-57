#!/usr/bin/env python

from setuptools import setup

with open('holidayrules/version.py') as f:
    exec(f.read())

with open('README.md') as f:
    long_description = f.read()

setup(
    name="holidayrules",
    version=__version__,
    url="https://github.com/GibbsConsulting/holidayrules",
    description="Rule-based description of holidays",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Gibbs Consulting",
    author_email="holidayrules@gibbsconsulting.ca",
    license='AGPL',
    packages=[
        'holidayrules',
    ],
    include_package_data=True,
    classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Affero General Public License v3',
    'Programming Language :: Python :: 3',
    ],
    keywords='django taskflow workflow',
    project_urls = {
    'Source': "https://github.com/GibbsConsulting/holidayrules",
    'Tracker': "https://github.com/GibbsConsulting/holidayrules/issues",
    'Documentation': 'http://holidayrules.readthedocs.io/',
    },
    install_requires = [
                        ],
    python_requires=">=3.7",
    )

