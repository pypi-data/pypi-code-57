import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name='swap-python-sdk',
    version='0.0.2',
    author='',
    author_email='',
    description='SWAP Python SDK',
    # long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        'google-cloud-pubsub==1.1.0',
        'jsonschema==3.2.0',
        'marshmallow==3.3.0',
        'python-dotenv==0.10.5',
        'requests==2.22.0'
    ],
    package_data={'swap': ['common/static/schemas/*']},
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ]
)
