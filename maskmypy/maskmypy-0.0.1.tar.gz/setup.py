from setuptools import setup, find_packages

setup(
    name="maskmypy",
    version="0.0.1",
    author="David Swanlund",
    author_email="david.swanlund@gmail.com",
    description="Geographic masking tools for spatial data anonymization",
    #long_description=long_description,
    #long_description_content_type="text/markdown",
    #url="https://github.com/pypa/sampleproject",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    python_requires='>=3.6',)