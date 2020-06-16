import setuptools

def readme():
    with open('README.rst') as f:
        return f.read()


setuptools.setup(
    name="gnodatapackages", # Replace with your own username
    version="1.0.5",
    author="charmandersgsg",
    author_email="charmandersgsg@gmail.com",
    description="data def packages for gno",
    long_description="data def packages for gno",
    long_description_content_type="text/markdown",
    url="https://github.com/charmandersgsg/gnodatapackages",
    packages=['gnodatapackages'],
    include_package_data=True,
    install_requires=[
          'pandas',
      ],
    test_suite='nose.collector',
    tests_require=['nose'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)