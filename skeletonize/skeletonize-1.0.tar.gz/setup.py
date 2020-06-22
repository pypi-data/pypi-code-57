import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="skeletonize",
    version="1.0",
    author="Kavi Gupta",
    author_email="skeletonize@kavigupta.org",
    description="Handles skeletonization and deskeletonization of python code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kavigupta/skeletonize",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
    install_requires=["cached-property==1.5.1", "attrs==19.3.0", "astunparse==1.6.3"],
)
