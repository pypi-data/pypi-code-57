import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='EZlogR',
    version='0.1',
    author='Jeremy Gillespie',
    author_email='jeremy@kodeslingr.com',
    url='http://www.ezlogr.com',
    packages=setuptools.find_packages(),
    license='MIT',
    description='This is a simple logging tool to help devs focus on writing code instead of writing logs.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.6'
)