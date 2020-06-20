import setuptools
import labs


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="labs",
    version=labs.__version__,
    author="Eran Brill",
    author_email="brillonedev@gmail.com",
    description="labs - a dask-distributed experiments manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Brillone/labs",
    download_url='https://github.com/Brillone/labs/archive/v0.0.4.tar.gz',
    packages=['labs'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
                        'bokeh==2.0.0',
                        'numpy==1.18.4',
                        'dask==2.18.0',
                        'distributed==2.18.0',
                        'slacker==0.14.0',
                        'scipy==1.4.1',
                        'scikit-learn==0.23.0',
                        'scikit-optimize==0.7.4'
                    ]
)
