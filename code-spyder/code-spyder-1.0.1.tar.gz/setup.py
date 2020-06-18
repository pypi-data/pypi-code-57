import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="code-spyder",
    version="1.0.1",
    author="Max G",
    author_email="max3227@gmail.com",
    description="Create source trees statistics by recursively crawling directories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'interutils',
        'prettytable',
    ],
    entry_points={
        'console_scripts': [
            'spyder = code_spyder:main',
        ]
    }
)
