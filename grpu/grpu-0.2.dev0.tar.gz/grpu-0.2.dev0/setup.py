import setuptools

setuptools.setup(
    name='grpu',
    version='0.2dev',
    license='MIT',
    long_description=open('README.md').read(),
    url='https://github.com/grios/grpu',
    download_url='https://pypi.python.org/pypi/grpu',
    author='Gibran Rios',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python',
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
)