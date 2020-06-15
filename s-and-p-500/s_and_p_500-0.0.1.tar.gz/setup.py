import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="s_and_p_500",
    version="0.0.1",
    author="Ben Scholar",
    author_email="bens@digitalman.com",
    description="Retrieve S&P500 prices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BBScholar/s_and_p_500.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires = [
        'pandas',
        'numpy',
        'beautifulsoup4',
        'requests',
        'lxml',
        'yfinance'
    ]
)