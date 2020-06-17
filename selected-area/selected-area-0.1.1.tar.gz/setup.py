import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="selected-area",  # Replace with your own username
    version="0.1.1",
    author="Dominik Nedvedik",
    author_email="dominik.nedvedik@protonmail.com",
    description="Calculates if plot/segment intersects the selected area.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nedvedikd/selected-area",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)