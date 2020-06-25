from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="CooHSQL",
    python_requires='>=3.6.0',
    version='1.0.0',
    author='HB',
    author_email='huabing8023@126.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    maintainer='HB',
    url='https://github.com/DooBeDooBa/CooHSQL',
    license='LICENSE',
    description='Apply flashback with DML',
    install_requires=[
        'PyMySQL',
        'mysql-replication'
    ],
    packages=find_packages()
)
