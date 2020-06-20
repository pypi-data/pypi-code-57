import setuptools

setuptools.setup(
    name="searchpoi",
    version="0.0.1",
    author="Massimo Colombi",
    author_email="massimo.colombi@librecamelot.org",
    description="This package search Point of Interests inside a specific area using Overpass API.",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    test_suite='nose.collector',
    tests_require=['nose']
)