import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="selenium_youtube",
    version="0.2.32",
    author="Kovács Kristóf-Attila",
    description="selenium_youtube",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kkristof200/selenium_youtube",
    packages=setuptools.find_packages(),
    install_requires=["beautifulsoup4", "kcu", "ktimeout", "selenium", "selenium_firefox"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)