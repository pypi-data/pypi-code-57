import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django_country_filter",
    version="0.0.1",
    author="Paulo Roberto",
    author_email="paulo.pinda@gmail.com",
    description="Django middleware country filter.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/0p4ul0/django-country-filter",
    packages=setuptools.find_packages(exclude=("tests",)),
    install_requires=['requests', 'django==2.2.13'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
