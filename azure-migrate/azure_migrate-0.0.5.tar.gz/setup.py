import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="azure_migrate", # Replace with your own username
    packages=["azure_migrate"],
    version="0.0.5",
    author="Alisson Castro",
    author_email="alissoncastroskt@gmail.com",
    description="A package to management migrate azure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alissonit/azure_migrate",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    project_urls={
        'Source': 'https://github.com/alissonit/azure_migrate',
        'Documentation':
        'https://github.com/alissonit/azure_migrate/docs',
        'Tracker': 'https://github.com/alissonit/azure_migrate/issues'
    }
)