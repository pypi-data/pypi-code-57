import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="small_probs-wlad111",
    version="0.2.0",
    author="Vladislav Strashko",
    author_email="wlad962961@gmail.com",
    description="framework for estimating small probabilities using MCMC based on PyMC3-like probability model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wlad111/pymc3",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pymc3-ext-wlad'
    ],
    python_requires='>=3.6',
)
