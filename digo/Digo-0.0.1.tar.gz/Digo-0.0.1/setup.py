from setuptools import setup, find_packages

setup(
    name='Digo',
    version='0.0.1',
    author='DiggerWorks',
    author_email='support@digger.works',
    package=find_packages(exclude=["Digo"]),
    long_description=open('README.md').read(),
    install_require=['azure-core', 'azure-storage-blob', 'Pillow', 'numpy', 'requests', 'psutil', 'nvgpu', 'argparse'],
    zip_safe=False
)