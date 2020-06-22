import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="regex_cleaner",  # Replace with your own username
    version="1.0.1",
    author="Lockie Richter",
    author_email="richter.lockie@gmail.com",
    description="A small package to convert verbose regex patterns to simple regex patterns.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lockieRichter/regex_cleaner",
    py_modules=["regex_cleaner"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["regex"],
    python_requires=">=3.6",
    entry_points="""
        [console_scripts]
        clean_regex=regex_cleaner:clean_regex
    """,
)
