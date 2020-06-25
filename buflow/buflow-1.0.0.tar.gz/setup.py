import setuptools, os

here = os.path.abspath(os.path.dirname(__file__))

os.chdir(here)

with open(
    os.path.join(here, "README.md"), "r", encoding="utf-8"
) as fp:
    long_description = fp.read()

setuptools.setup(
    name="buflow",
    version="1.0.0",
    author="Buflow",
    author_email="support@buflow.com",
    description="Python bindings for the Buflow API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/buflow/buflow-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
)
