from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='am_i_connected',
    version='0.1.2',
    description='The simplest way to check if internet access is available.',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Yann Cabral',
    author_email='iamyanndias@gmail.com',
    keywords=['internet', 'check', 'connection'],
    url='https://github.com/yanncabral/am_i_connected',
    download_url='https://pypi.org/project/am_i_connected/'
)

install_requires = [
    'socket'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)