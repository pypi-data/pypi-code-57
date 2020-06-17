from setuptools import setup  # type: ignore

version = '1.0'


setup(
    name='envvarconf',
    version=version,
    packages=[
        'envvarconf',
    ],
    url='https://github.com/a1fred/envvarconf',
    license='MIT',
    author='a1fred',
    author_email='demalf@gmail.com',
    description='Safe app configuration from environment variables without extra dependencies',
    classifiers=[
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    test_suite="tests",
)
