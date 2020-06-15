import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crawto-quality",
    version="0.0.10",
    author="Crawford Collins",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://chiselapp.com/user/Crawftv/repository/crawto-quality/home",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    install_requires=["astor"],
    python_requires=">=3.7",
    test_suite="tests",
    entry_points={"console_scripts": ["crawto-doc = crawto_doc.crawto_doc:main",],},
)
