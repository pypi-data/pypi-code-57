import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jefftadashi_utils",
    version="0.0.7",
    author="Jeff Tadashi Moy",
    author_email="jeff@jefftadashi.com",
    description="My general utilities Python module!",
    license="gpl-3.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JeffTadashi/jefftadashi_utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)