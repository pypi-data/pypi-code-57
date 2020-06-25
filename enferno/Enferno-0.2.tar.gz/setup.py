from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="Enferno",
    author_email="nidal@level09.com",
    description="Enferno framework CLI tool, helps you create and setup your Enferno app quickly.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/level09/enferno-cli",
    python_requires='>=3.5',
    license='MIT',
    version='0.2',
    py_modules=['enferno'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        enferno=enferno:create
    ''',
)
