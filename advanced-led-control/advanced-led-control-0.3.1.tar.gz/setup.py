import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as fh:
    requirements = fh.read().splitlines()

setuptools.setup(
    name="advanced-led-control", # Replace with your own username
    version="0.3.1",
    install_requires=requirements,
    author="Walid Shouman",
    author_email="eng.walidshouman@gmail.com",
    description="An non-official advanced controller for blinkstick",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/weshouman/advanced-led-control",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5.2',
)

