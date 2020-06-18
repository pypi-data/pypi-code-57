from setuptools import setup, find_packages

from zoomconnect_sdk import VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="zoomconnect_sdk",
    version=VERSION,
    author="LambrieSteyn",
    author_email="lambrie45@gmail.com",
    description="Python Wrapper module for ZoomConnect API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lambrie/zoomconnect_sdk",
    packages=find_packages(exclude=['tests']),
    install_requires=['requests>=2.18.4', 'six>=1.11.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords='Zoom ZoomConnect SMS Messages',
    test_suite='tests',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov', 'requests_mock']
)