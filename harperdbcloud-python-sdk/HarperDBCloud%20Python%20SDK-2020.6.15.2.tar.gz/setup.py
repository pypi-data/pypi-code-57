import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='HarperDBCloud Python SDK',
    version='2020.06.15.02',
    description='HarperDB Cloud Python SDK.',
    author='Xonshiz',
    author_email='xonshiz@gmail.com',
    url='https://github.com/Xonshiz/HarperDBCloud-Python',
    keywords=['HarperDB Cloud SDK'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)