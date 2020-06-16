import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pugna",
    version="0.0.19",
    author="Sebastian Khan",
    author_email="KhanS22@Cardiff.ac.uk",
    description="A lightweight package to perform regression with neural nets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/SpaceTimeKhantinuum/pugna",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
    scripts=[
        'bin/dev/pugna_fit',
        'bin/dev/pugna_scale_data'
        ]
)
