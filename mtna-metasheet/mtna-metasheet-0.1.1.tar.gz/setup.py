import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='mtna-metasheet',
    version='0.1.1',
    author='Pascal Heus',
    author_email='pacsal.heus@mtna.us',
    description='Metasheet parser, serializers, and repository manager',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={'': ['config.json']},
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.0',
    entry_points={
        "console_scripts": [
            "metasheet=metasheet.metasheet:main",
        ]
    }
    )


