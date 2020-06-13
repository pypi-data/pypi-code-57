import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="theano-hf",
    install_requires=["theano", "numpy"],
    version="0.2.0",
    author="Kiruya Momochi",
    author_email="kyaru@cock.li",
    description="General purpose Hessian-free optimization in Theano",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KiruyaMomochi/theano-hf-py3",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
