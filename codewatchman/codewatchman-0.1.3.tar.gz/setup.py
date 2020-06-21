import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="codewatchman",
    version="0.1.3",
    license="MIT",
    author="Code Watchman",
    author_email="codewatchmanapp@gmail.com",
    description="Code Watchman Python API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thevishnupradeep/CWMPythonLibrary",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers'
    ],
    keywords=["code watchman", "codewatchman", "watchman"],
    install_requires=[
        'requests'
    ],
    python_requires='>=3.4',
    download_url='https://github.com/thevishnupradeep/CWMPythonLibrary/archive/v0.0.1.tar.gz'
)