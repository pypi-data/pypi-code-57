import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fr:
    requirements = fr.read().splitlines()

setuptools.setup(
    name="TakeConfusionMatrix",
    version="0.0.2",
    author="Cecília Assis",
    author_email="cecilia.assis@take.net",
    description="TakeConfusionMatrix is a tool for batched metrics calculations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://curupira.visualstudio.com/DefaultCollection/Data%20Analytics%20%28DA%29/_git/TakeConfusionMatrix",
    maintainer="D&A Team",
    maintainer_email="analytics.ped@take.net",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
