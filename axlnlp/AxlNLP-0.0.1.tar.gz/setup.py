import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="AxlNLP", # Replace with your own username
    version="0.0.1",
    author="Axel Almquist",
    author_email="axelalmquist@gmail.com",
    description="my nlp tools",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/AxlAlm/AxlNLP",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy==1.18.1",
        "pytorch-lightning==0.7.3",
        "gensim==3.8.1",
        "spacy==2.2.3",
        "regex==2020.1.8",
        "nltk==3.4.5",
        "torch==1.4.0",
        "comet-ml==3.1.4",
        "nltk==3.4.5",
        "pytorch-crf==0.7.2",
        "flair==0.4.5",
        "scikit-learn==0.22.1",
        "pandas==1.0.1",
        "colorama==0.4.3",
        "Pillow==7.1.2",
        "swifter==0.304",
        "transformers==2.11.0",
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)