

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hospitalitydatascience", 
    version="2020.06.dev8",
    author="Jonathan N. Winters",
    author_email="jnw25@cornell.edu",
    description="Package for performing hospitality data analysis",
    long_description="Work In Progress: Package for performing hospitality data analysis and providing hospitality data standards\  Current Progress: Formulating Predicate Functor functions for hospitality data.",
    long_description_content_type="text/markdown",
    url="https://github.com/hospitalitydatascience/hospitalitydatascience",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

