from setuptools import setup, find_packages

with open('requirements.txt', 'r') as requirements_file:
    requirements = [requirement.strip() for requirement in \
                    requirements_file.readlines()]

with open('README.md', 'r') as readme:
    long_description = readme.read()


src_dir = "lib"
setup(
    name="config_precedence",
    description="Define the order of precedence of a list of configuration options",
    long_description=long_description,
    version="1.0.0",
    packages=find_packages(src_dir),
    package_dir={'': src_dir},
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.7",
    author="Eddy Mwenda",
    author_email="mwendaeddy@gmail.com",
)
