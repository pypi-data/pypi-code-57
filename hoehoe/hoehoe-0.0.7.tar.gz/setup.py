import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# with open('requirements/requirements.txt') as f:
#     required_packages = f.read().splitlines()

# required_packages = [ln for ln in required_packages if not ln.startswith('#')]
# pp(required_packages)

setuptools.setup(
    name="hoehoe",
    version="0.0.7",
    author="MJ Krakowski",
    author_email="packaging@c40.pl",
    description="Rox crawler",
    long_description='',
    long_description_content_type="text/markdown",
    url="https://github.com/dwabece/rox",
    install_requires=[
        'beautifulsoup4',
        'requests',
        'requests-html',
        'celery',
        'click',
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
