import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rotplot", # Replace with your own username
    version="0.0.1",
    author="Ant Gib",
    author_email="ant.gib@protonmail.com",
    description="Package to rotate 2D and 3D curves",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antscloud/rotplot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    'numpy >= 1',
      ],
    python_requires='>=3',
)
