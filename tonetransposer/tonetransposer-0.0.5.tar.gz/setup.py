from setuptools import setup

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
    'Programming Language :: Python :: 3'
]

setup(
    name='tonetransposer',
    version='0.0.5',
    packages=['tonetranspose'],
    url='',
    classifiers=classifiers,
    license='GPL2',
    author='Zaid Qureshi',
    author_email='zq99@hotmail.com',
    keywords=['MUSIC THEORY', 'PIANO', 'TRANSPOSITION', 'KEYBOARD', 'CHORDS', 'SCALES'],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown; charset=UTF-8; variant=GFM',
    description='Transposes a series of tones into all 12 keys and classifies them by their shape on a piano keyboard',
)
