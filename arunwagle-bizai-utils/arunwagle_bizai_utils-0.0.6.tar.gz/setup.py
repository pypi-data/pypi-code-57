import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arunwagle_bizai_utils", # Replace with your own username
    version ="0.0.6",
    author="Arun Wagle",
    author_email="arun.wagle@ibm.com",
    description="Utils Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['bizai.utils'],
    python_requires='>=3.6',
)