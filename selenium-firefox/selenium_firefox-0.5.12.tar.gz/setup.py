import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="selenium_firefox",
    version="0.5.12",
    author="Kovács Kristóf-Attila",
    description="selenium_firefox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kkristof200/selenium_firefox",
    packages=setuptools.find_packages(),
    install_requires=["fake_useragent", "selenium", "tldextract"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)