import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyhavamal",
    version="0.1.4",
    author="Evan Quinlan",
    author_email="evan.quinlan@gmail.com",
    description="A CSV file containing the Old Norse Hávamál stanzas and a simple Python app for accessing them.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/equinlan/pyhavamal",
    packages=['pyhavamal'],
    package_dir={'pyhavamal': 'pyhavamal'},
    package_data={'pyhavamal': ['data/stanzas']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    test_suite='nose.collector',
    tests_require=['nose'],
)