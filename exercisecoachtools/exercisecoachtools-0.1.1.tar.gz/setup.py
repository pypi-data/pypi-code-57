from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='exercisecoachtools',
    version='0.1.1',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.7, <4',
    url='https://github.com/chandojo/ExerciseCoachTools',
    license='MIT License',
    author='chandojo',
    description='Tools for exercise physiologists and coaches.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)
