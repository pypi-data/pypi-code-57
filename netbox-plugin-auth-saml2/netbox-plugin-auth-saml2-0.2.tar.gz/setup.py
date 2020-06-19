from setuptools import find_packages, setup


def requirements(filename='requirements.txt'):
    return open(filename.strip()).readlines()


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='netbox-plugin-auth-saml2',
    version='0.2',
    description='Netbox plugin for SAML2 auth',
    author='Jeremy Schulman',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache 2.0',
    install_requires=requirements(),
    packages=find_packages(),
    include_package_data=True,
)
