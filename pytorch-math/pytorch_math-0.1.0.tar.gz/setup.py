"""
Setup
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytorch_math",
    version="0.1.0",
    author="Daniel Kaminski de Souza",
    author_email="daniel@kryptonunite.com",
    description="Pytorch Math",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=['pytorch_math'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'torch'
    ],
    extras_require={
        'dev': [
            'pylint',
            'pep8',
            'autopep8',
            'bumpversion',
            'twine',
        ],
        'test': [
            'pytest>=4.6',
            'pytest-cov',
        ],
        'docs': [
        ]
    }
)
