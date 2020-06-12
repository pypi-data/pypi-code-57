import io

from setuptools import setup

setup(
    name='sqs-encrypted-extended-client',
    version='0.0.2',
    description='Allows for per-queue KMS encryption of large messages in S3',
    author='Joseph Wortmann',
    author_email='jwortmann@quinovas.com',
    url='https://github.com/QuiNovas/sqs-extended-client',
    license='Apache 2.0',
    long_description=io.open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=['sqs_encrypted_extended_client'],
    package_dir={'sqs_encrypted_extended_client': 'src/sqs_encrypted_extended_client'},
    install_requires = ['sqs-extended-client'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7',
    ],
)
