from setuptools import find_packages, setup

with open('README.rst', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ident',
    version='1.0',
    description='Identify with challenge messsage and SSH key.',
    long_description=long_description,
    # long_description_content_type='text/markdown',
    url='https://github.com/mindey/ident',
    author='Mindey',
    author_email='~@mindey.com',
    license='MIT',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        'cryptography',
    ],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            'ident=ident.cli:verify'
        ],
    }
)

