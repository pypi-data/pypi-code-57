import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()

setuptools.setup(
    name = 'good_bot_encrypt',
    version = '1.1.0',
    description = 'A simple password manager to be used with Good-Bot.',
    long_description = long_description,
    long_description_content_type="text/markdown",
    license = 'MIT',
    author = 'Tricky',
    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts': [
            'good_bot_encrypt = good_bot_encrypt.__main__:main'
            ]
        }
)
