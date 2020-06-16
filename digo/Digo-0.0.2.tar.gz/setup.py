from setuptools import setup, find_packages

setup(
    name='Digo',
    version='0.0.2',
    author='DiggerWorks',
    author_email='support@digger.works',
    packages=find_packages(),
    long_description=open('README.md').read(),
    keywords=['digo', 'ml'],
    install_require=['azure-core', 'azure-storage-blob', 'Pillow', 'numpy', 'requests', 'psutil', 'nvgpu', 'argparse'],
    zip_safe=False
)