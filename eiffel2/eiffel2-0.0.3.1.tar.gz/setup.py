import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eiffel2", # Replace with your own username
    version="0.0.3.1",
    author="Eduardo Alejandro Lozano Garcia",
    author_email="sagrario3098@gmail.com",
    description="Neural Network visualization tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ale9806/Eiffel2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
