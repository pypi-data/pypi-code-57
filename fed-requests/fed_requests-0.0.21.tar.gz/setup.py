import setuptools

with open('README.md') as readme:
    long_description = readme.read()

with open('requirements.txt') as reqs:
    requirements = reqs.read()

setuptools.setup(
    name='fed_requests',
    version='0.0.21',
    author='Santiago Silva',
    author_email='santiago-smith.silva-rincon@inria.fr',
    description='A python package for managing requests to the FEDBIONET API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.inria.fr/fedbionet/fed-requests',
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)
