import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="odoo_controller_crossuite",
    version="1.0.0",
    author="Tom Roels",
    author_email="tom@crossuite.com",
    description="A basic controller to ease querying Odoo databases.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/crossuite-projects/odoo_controller",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)