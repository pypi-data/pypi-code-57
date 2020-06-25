import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("LICENSE", "r") as f:
    license_ = f.read()

with open('requirements.txt') as fp:
    install_requires = fp.read()

setuptools.setup(
    name="deepcrawl",
    version="0.0.12",
    author="Andrei Mutu & Christopher Evans",
    author_email="support@deepcrawl.com",
    description="A package to simplify usage of the DeepCrawl REST API",
    long_description="DeepCrawl is a cloud based website crawler to diagnose & fix technical SEO and performance issues. This Python package simplifies the use of the DeepCrawl’s REST API.",
    long_description_content_type="text/x-rst",
    url="https://github.com/DeepCrawlSEO/dc_api_wrapper",
    packages=setuptools.find_packages(exclude=('tests', 'docs')),
    #license=license_,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=install_requires
)
