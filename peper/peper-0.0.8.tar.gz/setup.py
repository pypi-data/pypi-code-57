import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="peper",
    version="0.0.8",
    author="Nenad",
    author_email="Ahhhhmed@gmail.com",
    description="A bunch of recepies.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/ahhhhmed/peper",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'peper = peper.__main__:main'
        ]
    },
    test_suite='test',
)