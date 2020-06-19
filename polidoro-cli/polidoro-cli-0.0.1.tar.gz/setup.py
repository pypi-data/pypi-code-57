"""
Setup to create the package
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='polidoro-cli',
    version="0.0.1",
    description='Generic CLI.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/heitorpolidoro/cli',
    author='Heitor Polidoro',
    # author_email='heitor.polidoro',
    scripts=['bin/cli'],
    license='unlicense',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False
)
