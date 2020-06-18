import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pmtutils",
    version="0.0.1",
    author="Bennett Lambert",
    author_email="lambertb@uw.edu",
    description="Portable toolkit for interacting with the PyMetaTome pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lambertsbennett/pmtutils",
    download_url="https://github.com/lambertsbennett/pmtutils/archive/v_01.tar.gz",
    packages=setuptools.find_packages(),
    keywords=['Transcriptomics', 'Bioinformatics'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 2 - Pre-Alpha"
    ],
    install_requires=[
      'biopython',
      'numpy',
      'ruamel_yaml'
    ],
    python_requires='>=3.6',
)
