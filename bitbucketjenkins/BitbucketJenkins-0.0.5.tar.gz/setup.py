import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BitbucketJenkins",
    version="0.0.5",
    author="Ericson Rumuy",
    author_email="ericsonrumuy@gmail.com",
    description="A package for create Bitbucket project that integrate with Jenkins using Bitbucket team/project plugin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ericsonrumuy7/Bitbucket",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)