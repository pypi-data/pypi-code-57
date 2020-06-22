import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="multi-rename",
    version="0.0.2",
    author="Pushkar Kurhekar",
    author_email="dev@pshkrh.com",
    description="Easily rename multiple files ending with incrementing numbers.",
    keywords='multi batch rename all files',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pshkrh/multi-rename",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
    ],
    python_requires='>=3.3',
)