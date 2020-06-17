import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ynj",
    version="1.1.0",
    author="carbolymer",
    author_email="carbolymer@gmail.com",
    description="Compile Jinja templates with YAML variables",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/carbolymer/ynj",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: System :: Systems Administration"
    ],
    install_requires=['Jinja2', 'pyyaml'],
    entry_points={
        'console_scripts': [
            'ynj=ynj:main'
        ]
    }
)
