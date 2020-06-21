from setuptools import setup, find_packages

setup(
    name="pythere",
    version="0.2",
    author="Clint Lawrence",
    author_email="clint.lawrence@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    url="https://github.com/clint-lawrence/pythere",
    license="LICENSE",
    description="pythere is a tool to run python scripts over ssh",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    install_requires=[
        "fabric",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "pythere=pythere.__main__:main",
        ],
    }
)