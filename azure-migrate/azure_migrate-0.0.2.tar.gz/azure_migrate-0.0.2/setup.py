import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="azure_migrate", # Replace with your own username
    version="0.0.2",
    author="Alisson Castro",
    author_email="alissoncastroskt@gmail.com",
    description="A package to management migrate azure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alissonit/azure_migrate",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)