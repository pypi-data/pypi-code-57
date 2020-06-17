from setuptools import setup

with open("README.md", 'r') as fh:
    long_description = fh.read()

setup(
    name='temperature_converter_py',
    version='1.0.1',
    author='Bruno Nascimento',
    author_email='bruno_freddy@hotmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['temperature_converter_py'],
    url='https://github.com/BrunoASN/temperature_converter_py',
    project_urls={
        'Código fonte': 'https://github.com/BrunoASN/temperature_converter_py',
        'Download': 'https://github.com/BrunoASN/temperature_converter_py/archive/master.zip'
    },
    license='MIT',
    keywords=['conversor', 'temperatura'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Scientific/Engineering :: Physics'
    ],
    python_requires='>=3.4'
)
