from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='anonymize_UU',
    version='0.1.5',
    description='A tool to substitue patterns/names in a file tree',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url='https://github.com/cskaandorp/anonymize',
    author='C.S. Kaandorp',
    author_email='c.s.kaandorp@uu.nl',
    license='MIT',
    packages=['anonymize'],
    python_requires = '>=3.6',
    zip_safe=False
)