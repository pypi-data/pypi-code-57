import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bavard",
    version="0.0.14",
    author="Bavard AI, LLC",
    author_email="dev@bavard.ai",
    description="A library and CLI for NLP tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bavard-ai/bavard",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['bavard=bavard.cli.main:main'],
    },
    install_requires=[
        'tensorflow>=2.1',
        'tf-models-official',
        'tensorflow-hub>=0.7.0',
        'sentencepiece==0.1.85',
        'google-api-python-client>=1.8.0',
        'nltk>=3.5',
        'scikit-learn>=0.23.1',
    ],
)
