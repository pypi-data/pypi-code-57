from setuptools import setup
from os import path

current_dir = path.abspath(path.dirname(__file__))

with open(path.join(current_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="appixer-jlyric",
    packages=["appixer", "appixer.jlyric"],
    version="1.0.0",
    description="Metadata scrapper for j-lyric.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Joshua Avalon",
    author_email="git@avalon.sh",
    url="https://gitlab.com/appixer/jlyric",
    keywords=["audio", "metadata"],
    install_requires=["requests>=2.24.0, <=3.0.0", "BeautifulSoup4>=4.9.1, <=5.0.0"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
