import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pfp_lgbt',
    version='1.0.0',
    author='Weilbyte',
    description='Python API Wrapper for https://pfp.lgbt/',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Weilbyte/pfp_lgbt.py',
    packages=setuptools.find_packages(exclude=['test']),
    install_requires=[
        'aiohttp'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
)