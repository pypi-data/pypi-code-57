from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='mat',
    version='1.0.2',
    description='Manage your database versions with pure SQL',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Giovanni Aguirre',
    author_email='giovanni.fi05@gmail.com',
    url='https://github.com/DiganmeGiovanni/Mat',

    packages=find_packages(),
    install_requires=[
        'mysql-connector-python>=8.0.20',
        'PyYAML>=5.3.1',
        'tabulate>=0.8.7'
    ],
    entry_points={
        'console_scripts': [
            'mat=mat.runner:main'
        ]
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
