import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="despeech",
    version="0.0.2",
    author="Lidiia Ostyakova",
    author_email="lostaaa15@gmail.com",
    description="Tool for converting direct speech in German into indirect one",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lnpetrova/despeech",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'nltk',
        'uralicNLP'
    ]

)