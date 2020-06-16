import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='Flask-RestSecurity',
    version='0.0.2',
    author='Marcos Rosa',
    author_email='marcos.cantor@gmail.com',
    description='Rest API Security OpenSource Project with Flask',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/marcosstefani/flask-restsecurity',
    packages=['flask_restsecurity'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ],
    keywords='rest api authentication',
    python_requires='>=3.6',
)