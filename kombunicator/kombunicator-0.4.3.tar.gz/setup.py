import setuptools

from kombunicator.utils import get_version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kombunicator",
    version=get_version(file_name='release_info', version_string='RELEASE_VERSION'),
    author="Stefan Lasse",
    author_email="stefanlasse87+kombunicator@gmail.com",
    description="A threaded RabbitMQ message producer/consumer and RPC client/server.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mbio/kombunicator",
    download_url="https://gitlab.com/mbio/kombunicator/-/archive/master/kombunicator-master.tar.gz",
    keywords=["AMQP", "RPC", "kombu", "celery"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "celery==4.4.2",
        "kombu==4.6.8",
        "pytest==5.4.2",
        "pytest-timeout==1.4.1",
        "redis==3.5.0",
        "strongtyping>=1.1.17",
    ],
    python_requires='>=3.6',
    include_package_data=True
)
