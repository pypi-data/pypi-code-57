import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="linformer_pytorch", # Replace with your own username
    version="0.2.1",
    author="Peter Tatkowski",
    author_email="tatp22@gmail.com",
    description="An implementation of the Linformer in Pytorch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tatp22/linformer-pytorch",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'torch',
    ],
)
