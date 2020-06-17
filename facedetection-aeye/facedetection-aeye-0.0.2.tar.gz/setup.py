import setuptools, os

PACKAGE_NAME = 'facedetection-aeye'
VERSION = '0.0.2'
AUTHOR = 'jjmachan'
EMAIL = 'jamesjithin97@gmail.com'
DESCRIPTION = 'Pretrained Pytorch face detection and recognition models for use in the aeye module'
GITHUB_URL = 'https://github.com/jjmachan/facedetection-aeye'

parent_dir = os.path.dirname(os.path.realpath(__file__))
import_name = os.path.basename(parent_dir)

with open('{}/README.md'.format(parent_dir), 'r') as f:
    long_description = f.read()

setuptools.setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=GITHUB_URL,
    packages=[
        'facedetection',
        'facedetection.models',
        'facedetection.utils',
    ],
    package_dir={'facedetection':'./facedetection'},
    package_data={'': ['*net.pt']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy',
        'requests',
    ],
)
