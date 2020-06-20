import setuptools

setuptools.setup(
    name='siglent-vxi11',
    version='0.0.1',
    author='Richard Waschhauser',
    keywords='Siglent, vxi11',
    description='Siglent vxi11 library',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Topic :: System :: Hardware',
    ],
    python_requires='>=3.5',
)
