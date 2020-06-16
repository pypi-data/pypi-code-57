import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="youtube-uploader-selenium",
    version="0.1.0",
    author="Kostya Linou",
    author_email="linouk23@gmail.com",
    description="The package that helps to upload videos on YouTube using Selenium",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/linouk23/youtube_uploader_selenium",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
