import setuptools

long_description = 'Test vzmi namespace'

setuptools.setup(
    name="vzmi.foo",
    version="0.0.1",
    author="Jim Rollenhagen",
    author_email="jim@jimrollenhagen.com",
    description="A test on the vzmi namespace",
    long_description=long_description,
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
