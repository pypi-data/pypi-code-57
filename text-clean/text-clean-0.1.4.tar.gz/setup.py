import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="text-clean", 
    version="0.1.4",
    author="geb",
    author_email="853934146@qq.com",
    description="Process text for NLP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mikuh/text_clean",
    packages=setuptools.find_packages(),
    package_data={'': ['text_clean.so', 'data/*.txt']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)