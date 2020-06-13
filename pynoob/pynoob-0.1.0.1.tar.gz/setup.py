import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as fh:
    required = fh.read().splitlines()

setuptools.setup(
    name="pynoob",
    version="0.1.0.1",
    author="Syed Abdul K",
    author_email="abdksyed@gmail.com",
    description="A n00b DeepLearning Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abksyed/pynoob",
    download_url = "https://github.com/abksyed/pynoob/dist/pynoob-0.1.0.1.tar.gz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=required,
    include_package_data=True
)
