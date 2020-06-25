"""
Setup module
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sqlalchemy-query-helper",
    version="0.0.4",
    author="Akın Tekeoğlu",
    author_email="akin.tekeoglu@gmail.com",
    description="Query helper for sql alchemy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/akin-tekeoglu/sqlalchemy-query-helper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=["SQLAlchemy"],
)
