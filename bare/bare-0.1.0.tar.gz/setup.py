from setuptools import setup

setup(
    name='bare',
    version='0.1.0',
    packages=['bare'],
    url='https://git.sr.ht/~martijbraam/bare-py',
    license='MIT',
    author='Martijn Braam',
    author_email='martijn@brixit.nl',
    description='Encoder/decoder for BARE messages',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'bare=bare.__main__:main'
        ]
    }
)
