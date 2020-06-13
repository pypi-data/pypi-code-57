from setuptools import setup, find_packages
from triad import __version__


with open("README.md") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="triad",
    version=__version__,
    packages=find_packages(),
    description="A collection of python utils for Fugue projects",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Han Wang",
    author_email="goodwanghan@gmail.com",
    keywords="util utils utility utilities",
    url="http://github.com/fugue-project/triad",
    install_requires=["pandas", "six", "ciso8601", "pyarrow", "fs"],
    extras_require={},
    classifiers=[
        # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3.6",
)
