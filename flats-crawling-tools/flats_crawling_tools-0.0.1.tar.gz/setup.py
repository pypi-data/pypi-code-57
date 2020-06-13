from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup(
    name= "flats_crawling_tools",
    version="0.0.1",
    description= "some basic tools for crawling flats data",
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Mohamed Amjad LASRI',
    author_email='amjadepot@gmail.com',
    keywords=['crawling'],
    download_url="https://pypi.org/project/flats_crawling_tools"
)

install_requires = [
]