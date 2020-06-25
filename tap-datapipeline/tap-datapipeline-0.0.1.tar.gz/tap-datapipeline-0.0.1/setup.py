import setuptools

setuptools.setup(
    name="tap-datapipeline",
    version="0.0.1",
    author="Heaven",
    author_email="heaven@pleme.io",
    description="functions that power the data pipeline for tapresearch",
    url="https://github.com/heavenPleme/tap-datapipeline",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
