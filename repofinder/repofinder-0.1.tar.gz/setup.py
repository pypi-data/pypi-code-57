import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="repofinder",
    version="0.1",
    author="mateuszz0000",
    author_email="mtszzwdzk@gmail.com",
    description="Find repo for your first contribution!.",
    long_description="Find repo for your first contribution!.",
    long_description_content_type="text/markdown",
    url="https://github.com/mateuszz0000/repofinder",
    download_url = 'https://github.com/mateuszz0000/repofinder/archive/v_0.1.tar.gz',
    install_requires=required,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
