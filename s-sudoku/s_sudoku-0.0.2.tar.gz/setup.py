from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='s_sudoku',
    version='0.0.2',
    description='Sudoku solver',
    long_description=open('README.txt').read(),
    url='',
    author='Kushagar Goel',
    author_email='kushagargoel28@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='sudoku',
    packages=find_packages(),
    install_requires=['']
)