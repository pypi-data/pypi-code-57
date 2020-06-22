import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cssaw_central",
    version="1.0.0",
    author="Luke Williams",
    author_email="williams.luke.2001@gmail.com",
    description="Access Point Module to CSSAW Database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CSSAW/CSSAW_Central",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy==1.19.0',
        'pandas==1.0.5',
        'PyMySQL==0.9.3',
        'python-dateutil==2.8.1',
        'pytz==2020.1',
        'six==1.15.0',
        'SQLAlchemy==1.3.17',
    ]
)