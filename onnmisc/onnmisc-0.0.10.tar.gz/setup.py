from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='onnmisc',
    version='0.0.10',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    url='https://onnmisc.oznetnerd.com',
    install_requires=[],
    license='',
    author='Will Robinson',
    author_email='will@oznetnerd.com',
    description='Miscellaneous functions used to fulfill common requirements'
)
