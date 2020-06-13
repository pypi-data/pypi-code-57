import setuptools
import simple_sample

setuptools.setup(
    name="simple-sample",
    version=simple_sample.__version__,
    author=simple_sample.__author__,
    author_email="alessandra.bilardi@gmail.com",
    description="A simple sample of a Python package prototype",
#     long_description=open('README.md').read(),
#     long_description_content_type="text/markdown",
    long_description=open('README.rst').read(),
    long_description_content_type="text/x-rst",
    url="https://simple-sample.readthedocs.io/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    project_urls={
        "Source":"https://github.com/bilardi/python-prototype",
        "Bug Reports":"https://github.com/bilardi/python-prototype/issues",
        "Funding":"https://donate.pypi.org",
    },
)
