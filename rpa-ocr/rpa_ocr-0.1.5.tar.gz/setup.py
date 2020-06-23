# -*- coding:utf-8 -*-
# @author :adolf
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rpa_ocr",
    version="0.1.5",
    author="adolf",
    author_email="adolf1321794021@gmail.com",
    description="A Tools for use algorithm for verification recognition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://code.ii-ai.tech/zhutaonan/rpa_verification.git",
    packages=setuptools.find_packages(),
    # data_files=['Identify_English/english_alphabet.txt',
    # 'Identify_English/english_alphabet_big.txt'],
    package_data={'': ['*.txt']},
    install_requires=['torch',
                      'torchvision',
                      'opencv-python',
                      'pyyaml',
                      'tqdm'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
