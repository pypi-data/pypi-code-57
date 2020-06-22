import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='geodn',
    version='0.20200616.1',
    author='汪心禾',
    author_email='wangxinhe06@gmail.com',
    description='Geo Domain Name',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/wxh06/geodn',
    packages=setuptools.find_packages(),
    package_data={'geodn': ['GeoLite2*/*']},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
)
