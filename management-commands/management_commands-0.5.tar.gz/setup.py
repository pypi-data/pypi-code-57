from setuptools import setup


VERSION = "0.5"

setup(
    name='management_commands',
    version=VERSION,
    url='https://github.com/a1fred/management_commands',
    license='MIT',
    packages=['management_commands', ],
    author='a1fred',
    author_email='demalf@gmail.com',
    include_package_data=True,
    description='Extra small zero-dependency management commands library for python apps',
    classifiers=[
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
    ],
)
