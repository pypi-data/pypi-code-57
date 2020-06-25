from setuptools import setup, find_packages

long_description = "Minimal CLI / library to handle dependency information for NYU SSL experiments"

setup(
    name="depcrank",
    version="0.1.0",
    author="Aditya Sirish",
    author_email="aditya.sirish@nyu.edu",
    description=long_description,
    long_description=long_description,
    url="https://github.com/adityasaky/thesis-tooling",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "depcrank-rank = depcrank.depcrank_rank:main",
            "depcrank-display = depcrank.depcrank_display:main",
            "depcrank-analyse = depcrank.depcrank_analyse:main"
        ]
    }
)
