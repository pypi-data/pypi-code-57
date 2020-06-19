from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='vaknl-gcp',
    description='Vakanties.nl pypi package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='1.2.6',
    url='https://github.com/vakantiesnl/vaknl-PyPi.git',
    author='Wytze Bruinsma',
    author_email='wytze.bruinsma@vakanties.nl',
    keywords=['vaknl', 'pip'],
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=['google-cloud-bigquery', 'google-cloud-storage', 'google-cloud-secret-manager', 'newlinejson',
                      'google-cloud-tasks==1.3.0', 'googleapis-common-protos==1.6.0']
    )
