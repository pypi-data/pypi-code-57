import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="linformer_pytorch", # Replace with your own username
    version="0.8.7",
    author="Peter Tatkowski",
    author_email="tatp22@gmail.com",
    description="An implementation of the Linformer in Pytorch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tatp22/linformer-pytorch",
    packages=setuptools.find_packages(),
    keywords=['transformers', 'attention', 'deep learning', 'artificial intelligence', 'sparse attention'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    install_requires=[
        'torch',
        'matplotlib',
    ],
)
