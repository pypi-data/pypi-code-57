import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yamlparams", # Replace with your own username
    version="0.0.2",
    author="Ilia Ilmenskii",
    author_email="gipermonk@bk.ru",
    description="Config helper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Aroize",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
