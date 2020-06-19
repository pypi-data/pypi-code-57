import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sms_messenger", # Replace with your own username
    version="1.1.0",
    author="Kenan Turner",
    author_email="coolspykee@satx.rr.com",
    license='MIT',
    description="A simple Python package for sending messages over SMS Gateways.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/coolspykee/sms_messenger",
    packages=setuptools.find_packages(),
    install_requires=[
        'imapclient>=2.1.0',
        'pyzmail>=1.0.3',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)