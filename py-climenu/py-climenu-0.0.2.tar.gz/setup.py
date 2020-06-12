import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="py-climenu",
    version="0.0.2",
    author="baely",
    author_email="contact@baely.dev",
    description="Python menu for CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/baely/PyCLIMenu",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
