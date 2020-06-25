import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="npu", 
    version="0.1.13",
    author="Neuro AI",
    author_email="api@neuro-ai.co.uk",
    description="Python client for using npu api",
    long_description=long_description,
    long_description_content_type="text/markdown",
 #   url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests>=2', 'numpy>=1.18', 'dill', 'bson', 'progress'],
    python_requires='>=3.6',
)
