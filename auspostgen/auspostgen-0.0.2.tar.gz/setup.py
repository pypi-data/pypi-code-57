import setuptools
import platform

# Determine the correct platform for the webdriver
system = platform.system()
arch, _ = platform.architecture()
driver = None
if system == 'Linux':
    if arch == '64bit':
        driver = 'auspostgen/auspost.so'
if driver is None:
    raise OSError('Could not find the binary file for the current platform.')

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="auspostgen",
    version="0.0.2",
    author="Damian Dennis",
    author_email="damiandennis@gmail.com",
    description="Generation of the Australia Post Barcode versions 37, 52, 67",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/damiandennis/auspost",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'pillow>=7.1.2,<7.2.0',
        'click>=7.0.0,<7.2.0'
    ],
    data_files=[('bin', [driver])],
    python_requires='>=3.6',
    entry_points="""
    [console_scripts]
    auspostgen-image=auspostgen:write_image
    """
)
