import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='veazy',
	version='0.1.3',
    author='Xomnia14',
	author_email='jan.scholten@xomnia.com',
	description='Easy way to visualise your python package',
	log_description=long_description,
	long_description_content_type='text/markdown',
	url='https://gitlab.com/janscholten/veazy',
	packages=setuptools.find_packages(),
    install_requires=[
        'pydotplus',
        'click',
        'networkx',
        'pyan3-for-veazy'
    ],
    entry_points = {
        'console_scripts': ['veazy=veazy.cli:cli'],
    },
	classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    tests_require=['pytest'],
)

