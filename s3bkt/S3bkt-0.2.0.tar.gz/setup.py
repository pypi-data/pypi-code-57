from setuptools import setup
setup(
    name="S3bkt",
    version='0.2.0',
    packages=['s3bkt'],
    description='S3 bucket utility',
    author='Chuck Muckamuck',
    author_email='Chuck.Muckamuck@gmail.com',
    install_requires=[
        "boto3>=1.9",
        "Click>=7.0"
    ],
    entry_points="""
        [console_scripts]
    s3bkt=s3bkt.command:main
    """
)
