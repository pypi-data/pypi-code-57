import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="word_mover_distance",
    version="0.0.1",
    author="Khaled Hechmi",
    author_email="hechmi.khaled1995@gmail.com",
    description="Compute Word Mover's Distance using any type of Word Embedding model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hechmik/word_mover_distance",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='nlp wordembeddings wordmoverdistance similarity',
    install_requires=['numpy', 'gensim', 'pyemd'],
    python_requires='>=3.6',
)
