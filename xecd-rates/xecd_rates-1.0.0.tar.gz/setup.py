import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='xecd_rates',
    version='1.0.0',
    url='https://github.com/doguskidik/xecd-rates-python',
    packages=setuptools.find_packages(exclude=['tests*']),
    description='XECD REST Client Free',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Doğuş KIDIK',
    author_email='dogus.kidik@gmail.com',
    zip_safe=True,
    test_suite='tests',
    install_requires=[
        'requests',
		'lxml'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent"
    ]
)
