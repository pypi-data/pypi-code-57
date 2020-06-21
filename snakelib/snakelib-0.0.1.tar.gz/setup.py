import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="snakelib", # Replace with your own username
    version="0.0.1",
    author="snake-soft",
    author_email="info@snake-soft.com",
    description="Development tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/snake-soft/snake-lib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
