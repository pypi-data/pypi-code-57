import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="md-cata-notfresh", # Replace with your own username
    version="0.0.2",
    author="notfresh",
    author_email="notfresh@foxmail.com",
    description="generate the markdown catagory automatically",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/notfresh/md-cata",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=['bin/md-cata'],
    python_requires='>=3.5',
)
