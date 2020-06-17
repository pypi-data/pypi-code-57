import setuptools

setuptools.setup(
    name='scicap',
    version='2020.6.1',
    author='scicapital',
    author_email='public@scicapital.com',
    description='futures tool',
    license='MIT Licence',
    url='http://scicapital.com',
    packages=setuptools.find_packages(),
    platforms='any',
    python_requires=">=3.6",
    install_requires=["pandas>=0.21.0"],
)
