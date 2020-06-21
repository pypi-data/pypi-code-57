import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="code128bgen",
    version="0.0.1",
    author="Damian Dennis",
    author_email="damiandennis@gmail.com",
    description="Generation of the Code128b barcode",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/damiandennis/code128bgen",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'pillow>=7.0.0,<7.2.0'
    ],
    python_requires='>=3.6',
)
