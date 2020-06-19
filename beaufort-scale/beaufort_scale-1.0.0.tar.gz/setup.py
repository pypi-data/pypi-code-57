from setuptools import setup

with open("README.md", 'r') as fh:
    long_description = fh.read()

setup(
    name='beaufort_scale',
    version='1.0.0',
    author='Bruno Nascimento',
    author_email='bruno_freddy@hotmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['beaufort_scale'],
    url='https://github.com/BrunoASN/beaufort-scale',
    project_urls={
        'Código fonte': 'https://github.com/BrunoASN/beaufort-scale',
        'Download': 'https://github.com/BrunoASN/beaufort-scale/archive/master.zip'
    },
    license='MIT',
    keywords=['conversor', 'wind', 'speed', 'beaufort'],
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
