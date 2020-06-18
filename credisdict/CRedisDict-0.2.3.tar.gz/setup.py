import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requires = [
    'redis',
    'jsonpickle',
]

setuptools.setup(
    name="CRedisDict",
    version="0.2.3",
    author="Joan Hérisson",
    author_email="joan.herisson@univ-evry.fr",
    description="Dictionnary with complex data stored in a Redis database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brsynth/CRedisDict",
    packages=setuptools.find_packages(),
    test_suite = 'discover_tests',
    test_requires=requires,
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
