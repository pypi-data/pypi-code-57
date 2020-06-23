import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kermout_strips_api",
    version="0.0.4", #Change this when updating.
    author="RazerMoon",
    author_email="rasync@rasync.xyz",
    description="Remotely interact with Kermout's Strips System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RazerMoon/Kermout_Strips_API",
    packages=setuptools.find_packages(),
    project_urls={
        "Documentation": "https://github.com/RazerMoon/Kermout_Strips_API/wiki",
        "Source Code": "https://github.com/RazerMoon/Kermout_Strips_API",
    },
    install_requires=[
        'requests',
        'bs4',
        'prettytable',
        'lxml'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)