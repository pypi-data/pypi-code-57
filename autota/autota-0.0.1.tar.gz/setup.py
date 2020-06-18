import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autota", # 
    version="0.0.1",
    author="Jay",
    author_email="a121406@gmail.com",
    description="Automatic generate QA from slides and grade marker/memo.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/miyuiki/autota",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)