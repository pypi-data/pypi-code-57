import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xre",  # Replace with your own username
    version="0.0.1",
    author="Ricardo Ander-Egg",
    author_email="ricardo.anderegg@gmail.com",
    description="Build regex like legos.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/polyrand",
    packages=setuptools.find_packages(),
    # install_requires=["peppercorn"],  # requirements/main.in
    # extras_require={"dev": ["check-manifest"]},  # requirements/dev.in
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
    ],
    python_requires=">=3.7",
)
