from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="lib_1",
    version="1.0.3",
    description="information about author",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/SurendraKumawat23",
    author="Surendra Kumawat",
    author_email="surendrakumawatp@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["lib_1"],
    include_package_data=True,
    #install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "lib=lib_1.info:name",
        ]
    },
)
