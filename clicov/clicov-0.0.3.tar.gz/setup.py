from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='clicov',
    version='0.0.3',
    author= 'Heru Handika',
    author_email= 'hhandika.us@gmail.com',
    description= 'Command line application to track COVID-19 cases',
    long_description= long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/hhandika/clicov',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'Click', 
        'pandas', 
        'requests', 
        'tabulate'
    ],
    entry_points='''
        [console_scripts]
        clicov=clicov.clicov:main
    ''',
)