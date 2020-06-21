import setuptools

setuptools.setup(
    name='siglent-vxi11',
    version='0.0.6',
    author='Richard Waschhauser',
    keywords='Siglent, VXI, SDL1020X-E, ',
    description='Siglent vxi11 library',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    packages=setuptools.find_packages(),
    install_requires=[
        'python-vxi11',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Topic :: System :: Hardware :: Hardware Drivers',
        'Topic :: System :: Networking',
    ],
    python_requires='>=3.5',
)
