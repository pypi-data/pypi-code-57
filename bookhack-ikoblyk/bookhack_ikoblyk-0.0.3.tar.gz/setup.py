import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bookhack_ikoblyk",
    version="0.0.3",
    author="Ivan Koblyk",
    author_email="ivankob.16@gmail.com",
    description="Book downloading tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ikoblyk/IMAGES_TO_DVU_BOOK.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.5',
    install_requires = [
        'Cython==0.29.14',
        'selenium==3.141.0',
        'urllib3==1.25.7',
    ],
)