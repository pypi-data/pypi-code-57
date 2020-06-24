from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="bms-tree-modules",
    version="0.2.0",
    packages=find_packages(exclude=["tests", "files", "src/utils"]),
    package_data={"": ["LICENSE", "NOTICES"]},
    python_requires=">=3.8",
    setup_requires=[],
    install_requires=["typing"],
    extras_require={
        "dev": ["pylama", "black", "flake8"],
        "tests": ["pytest", "pytest-watch"],
    },
    include_package_data=True,
    author="Moritz Eck",
    author_email="moritz.eck@gmail.com",
    description="The package contains the generic building blocks for the period-based Banking Management Simulation Games developed by the Institue of Banking & Finance (University of Zurich, Switerland).",  # noqa: E501
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.uzh.ch/uzh-bf/sim/banking-game-2020",
    project_urls={
        "Documentation": "https://gitlab.uzh.ch/uzh-bf/sim/banking-game-2020",
        "Source Code": "https://gitlab.uzh.ch/uzh-bf/sim/banking-game-2020",
    },
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
    ],
)
