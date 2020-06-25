from typing import Dict

from setuptools import find_packages, setup

VERSION: Dict[str, str] = {}
with open("vtorch/version.py", "r") as version_file:
    exec(version_file.read(), VERSION)

setup(
    name="vtorch",
    packages=find_packages(),
    include_package_data=True,
    version=VERSION["VERSION"],
    description="NLP research library, built on PyTorch. Based on AllenNLP.",
    author="Vitalii Radchenko",
    author_email="radchenko.vitaliy.o@gmail.com",
    install_requires=[
        "torch>=1.3.0",
        "overrides",
        "tqdm>=4.19",
        "numpy",
        "jsonpickle",
        "sklearn",
        "tensorboard",
        "fastprogress==0.1.18",
        "transformers==2.10.0",
    ],
)
