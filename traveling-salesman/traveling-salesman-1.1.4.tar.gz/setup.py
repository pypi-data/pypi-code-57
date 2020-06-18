import setuptools


# with open('requirements.txt') as f:
#     required = f.read().splitlines()

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setuptools.setup(
    name="traveling-salesman",
    version="1.1.4",
    description="A Python package to plot traveling salesman problem with greedy and smallest increase algorithm.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/furkankykc/TravelingSalesman.git",
    author="Furkan Kıyıkcı",
    author_email="furkanfbr@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    # install_requires=['numpy'],
    python_requires='>=3.6'
)
