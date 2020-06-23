import setuptools

with open('README.rst', encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='PartNLP',
    version='0.0.1',
    author="Mostafa Rahgouy",
    author_email="mostfarahgouy@gmail.com",
    description="Text preprocesssing",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['hazm', 'parsivar', 'stanza', 'nltk'],
    python_requires='>=3.6',
    nltk_requires='== 3.4'
)
