import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="NRlabdtsc",
    version="1.0.0",
    description="This tool is intended for training in waveform generation of the fifth generation new radio (5GNR). ",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/guipalloz/NRlab-dtsc",
    author="Guillermo Palomino Lozano",
    author_email="jabecerra@us.es",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["NRlabdtsc"],
    include_package_data=True,
    install_requires=["feedparser", "html2text"],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)
