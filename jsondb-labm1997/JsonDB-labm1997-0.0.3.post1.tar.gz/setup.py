import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="JsonDB-labm1997", # Replace with your own username
    version="0.0.3-1",
    author="Luiz Antônio Borges Martins",
    author_email="labm1997@gmail.com",
    description="This is a simple I/O JSON handler that allows direct operations on JSONs and with a single call to `JsonDB.flushAll`you can save them all on permanent memory.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/unball/jsondb",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
