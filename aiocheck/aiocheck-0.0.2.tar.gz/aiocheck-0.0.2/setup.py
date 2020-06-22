import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aiocheck",
    version="0.0.2",
    author="kruserr",
    description="A python asyncio host health checker using native ping commands",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kruserr/aiocheck",
    packages=setuptools.find_packages(),
    package_dir={
        '': 'src',
    },
    install_requires=[],
    entry_points = {
        'console_scripts': ['aiocheck=aiocheck.command_line:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
