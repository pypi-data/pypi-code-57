from setuptools import setup
from setuptools import find_packages

NAME = "cnlp-cli"
AUTHOR = "Ailln"
EMAIL = "dovolopor@gmail.com"
URL = "https://github.com/dovolopor-research/cnlp-cli"
LICENSE = "MIT License"
DESCRIPTION = "cnlp-cli is CNLP Command Line Interface, which is a submodule of cnlp."

if __name__ == "__main__":
    setup(
        name=NAME,
        version="0.0.1",
        author=AUTHOR,
        author_email=EMAIL,
        url=URL,
        license=LICENSE,
        description=DESCRIPTION,
        packages=find_packages(),
        include_package_data=True,
        install_requires=open("./requirements.txt", "r").read().splitlines(),
        long_description=open("./README.md", "r").read(),
        long_description_content_type='text/markdown',
        entry_points={
            "console_scripts": [
                "cnlp=cnlp_cli.shell:run"
            ]
        },
        package_data={
            "cnlp_cli": ["src/*.txt"]
        },
        zip_safe=True,
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires=">=3.6"
    )
