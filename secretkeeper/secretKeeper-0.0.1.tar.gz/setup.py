import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()

setuptools.setup(
    name = 'secretKeeper',
    version = '0.0.1',
    description = 'A simple password manager to be used with Good-Bot.',
    long_description = long_description,
    long_description_content_type="text/markdown",
    license = 'MIT',
    author = 'Tricky',
    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts': [
            'secretKeeper = secretKeeper.__main__:main'
            ]
        }
)
