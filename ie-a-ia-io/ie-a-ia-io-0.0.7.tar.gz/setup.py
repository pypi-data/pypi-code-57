import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ie-a-ia-io",     
    version="0.0.7",
    author="sgarda",
    author_email="sgarda@posteo.net",
    description="Incredibly basic class for managing simple input/output streams",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/sgarda/ieaiaio_v1",
    packages=setuptools.find_packages(),
    classifiers=[
'Operating System :: OS Independent',
'Topic :: Utilities'],
    python_requires='>=3.7',
)
