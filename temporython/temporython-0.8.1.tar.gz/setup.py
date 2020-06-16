from setuptools import setup, find_packages

with open("README.md", "r") as f:
    longdesc = f.read()

setup(
    name="temporython",
    version="0.8.1",
    description="Generate temporary Python scripts to quickly process lines of text or whole text files.",
    long_description=longdesc,
    long_description_content_type="text/markdown",
    url="https://github.com/waterimp/temporython",
    author="Lee Bush",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Text Processing",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="python code generator data processing",
    packages=['temporython'],
    package_dir={'temporython': 'temporython'},
    package_data={'temporython': ['templates/*.template']},
    scripts=['temporython/temporython'],
    python_requires=">=3.5",
)
