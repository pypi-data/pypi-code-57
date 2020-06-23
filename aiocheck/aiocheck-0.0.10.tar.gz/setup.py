import setuptools


with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

with open('VERSION', 'r') as f:
    VERSION = f.read()

setuptools.setup(
    name='aiocheck',
    version=VERSION,
    author='kruserr',
    description='A python asyncio host health checker using native ping commands',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/kruserr/aiocheck',
    keywords='asyncio host health checker native ping',
    project_urls={
        'Documentation': 'https://github.com/kruserr/aiocheck/wiki',
        'Source': 'https://github.com/kruserr/aiocheck',
    },
    packages=setuptools.find_packages(
        where='src',
    ),
    package_dir={
        '': 'src',
    },
    install_requires=[],
    entry_points = {
        'console_scripts': ['aiocheck=aiocheck.cli:main'],
    },
    zip_safe=True,
    classifiers=[
        'Topic :: System :: Networking :: Monitoring',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
