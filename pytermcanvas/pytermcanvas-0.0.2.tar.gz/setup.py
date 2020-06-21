import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="pytermcanvas",
        version="0.0.2",
        author="Lukáš Dršman",
        author_email="lukaskodr@gmail.com",
        description="Minimal terminal canvas",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/LukasDrsman/pytermcanvas",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: Public Domain",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.7'
        )
