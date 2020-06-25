import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="subsheets", # Replace with your own username
    version="0.7",
    author="Akash Chavan",
    author_email="achavan1211@gmail.com",
    description="utility to create subsheets in excel file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CruiseDevice/subsheets",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    keywords='subsheets sheets',
    python_requires='>=3.6',
    install_requires=['pandas', 'xlrd', 'XlsxWriter'],
    entry_points={
        'console_scripts': [
            'subsheets=src.subsheets:main'
        ]
    }
)