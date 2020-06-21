from setuptools import setup, find_packages

with open("VERSION") as vfile:
    version_line = vfile.readline()

with open("README.md", "r") as fh:
    long_description = fh.read()

version = version_line.strip()

setup(
    name="graafilohi",
    py_modules=["graafilohi"],
    include_package_data=True,
    package_data={
        "graafilohi": ["CHANGELOG.md", "VERSION", "README.md"]
    },
    version=version,
    license="MIT",
    description="Library for defining runnable pipelines as graphs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Aki Mäkinen",
    author_email="nenshou.sora@gmail.com",
    url="https://gitlab.com/blissfulreboot/python/graafilohi",
    keywords=[],
    install_requires=[
        "networkx",
        "matplotlib"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6"
    ]
)
