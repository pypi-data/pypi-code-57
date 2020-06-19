import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="researcher",
    version="0.0.2",
    author="Louka Ewington-Pitsos",
    author_email="lewingtonpitsos@gmail.com",
    description="Helps to run and analyse data science experiments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=[
        "tensorflow==2.2.0",
        "tensorboard==2.2.2",
        "numpy==1.18.5",
        "torch==1.5.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)