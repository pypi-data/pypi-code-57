from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
"batemaneq>=0.2.2",
"Pint>=0.12",
"importlib_resources; python_version<'3.7'",
]

setup(
    name ='decaychain',
    version ='0.5.13',
    description='Module to radioactively decay radioactive elements using the ICRP 107 and Bateman Equation',
#   package_dir={''},
    license='MIT',

    packages=find_packages(),
    author="Kenneth McKee",
    author_email="kenneth.mckee@protonmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rolleroo/decaychain",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
include_package_data = True,
package_data = {
'' : ['*.NDX'],
}
)