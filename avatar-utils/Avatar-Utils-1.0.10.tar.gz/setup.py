import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Avatar-Utils",
    version="1.0.10",
    author="Algorithmics of Complex System",
    author_email="artem.sementsov@gmail.com",
    description="Common utils for services in ecosystem",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=['avatar_utils.core', 'avatar_utils.db', 'avatar_utils.logs', 'avatar_utils.tests',
              'avatar_utils.validation', 'avatar_utils.registration'],
    install_requires=[
        'flask>=1.1.1',
        'flask-sqlalchemy>=2.3.2',
        'requests>=2.23.0',
        'psycopg2-binary>=2.7.5',
        'apispec==3.3.0',
        'marshmallow==3.6.0',
        'flasgger==0.9.4'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
