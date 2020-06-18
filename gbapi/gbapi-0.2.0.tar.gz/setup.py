import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gbapi",
    version="0.2.0",
    author="qeaml",
    author_email="qeaml@wp.pl",
    description="qeaml's wrapper for GameBanana's API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/QeaML/gbapi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	license='MIT',
    python_requires='>=3.6',
	install_requires=['aiohttp'],
)