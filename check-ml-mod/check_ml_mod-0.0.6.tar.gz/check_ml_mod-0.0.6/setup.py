from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))

version = '0.0.6'

install_requires = [
    "cselector"
]

readme = open("README.md").read()

setup(name='check_ml_mod',
    version=version,
    description="CLI tool.",
    long_description="https://github.com/aieater/python_check_ml_mod\n\n"+readme,
    long_description_content_type='text/markdown',
    classifiers=(
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ),
    keywords='',
    author='Pegara, Inc.',
    author_email='info@pegara.com',
    url='https://github.com/aieater/python_check_ml_mod',
    license='MIT',
    scripts=['bin/check_ml_mod'],
    zip_safe=False,
    install_requires=install_requires,
    entry_points={}
)
