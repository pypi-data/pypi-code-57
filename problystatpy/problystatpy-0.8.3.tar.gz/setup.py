import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='problystatpy',
    version='0.8.3',
    author="Jenny J. Jung",
    author_email='jjung@gmail.com',
    description='Statististical Probability Distributions',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jungsnn/problystatPyP",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
)
