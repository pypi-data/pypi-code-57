from versy import versy

_classifiers = [
    'Development Status :: 4 - Beta',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Topic :: Software Development :: Libraries',
    'Topic :: Utilities',
]

with open('requirements.txt') as f:
    REQUIRED = f.read().splitlines()

if __name__ == '__main__':
    from setuptools import setup

    setup(
        name='versy',
        version=versy.__version__,
        author='Tom Ritchford',
        author_email='tom@swirly.com',
        url='https://github.com/rec/versy',
        tests_require=['pytest'],
        py_modules=['versy'],
        description='Update the Python version number',
        long_description=open('README.rst').read(),
        license='MIT',
        classifiers=_classifiers,
        keywords=['documentation'],
        scripts=['scripts/versy'],
        packages=['versy'],
        install_requires=REQUIRED,
    )
