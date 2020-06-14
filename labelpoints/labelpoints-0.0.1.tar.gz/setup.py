import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="labelpoints", # Replace with your own username
    version="0.0.1",
    author="ScCcEe",
    author_email="1229659207@qq.com",
    description="a simply tool for points",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://github.com/ScCcWe/labelpoints",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
