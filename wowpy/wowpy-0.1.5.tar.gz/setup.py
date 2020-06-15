import setuptools

with open('VERSION', 'r') as fh:
    version = fh.read().strip()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wowpy",
    version=version,
    install_requires=[
      "setuptools",
      "requests"
    ],
    author="Daniel Barragan",
    author_email="dbarragan1331@gmail.com",
    description="Wowza python wrapper - wowpy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/d4n13lbc/wowpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={'': ['config.json']},
    include_package_data=True,
    zip_safe=False
)