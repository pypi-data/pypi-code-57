import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="welp",
    version="0.0.3",
    author="Alex Ye",
    author_email="alexzye1@gmail.com",
    description="what should i eat?",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/azye/welp",
    entry_points={'console_scripts': ['welp=welp.__main__:welp']},
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
