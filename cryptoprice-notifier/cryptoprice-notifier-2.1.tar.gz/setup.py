from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='cryptoprice-notifier',
    version='2.1',
    description='tool to get crypto price notification',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts':
        [
            'cryptonotifier = cryptonotifier.main:main'
        ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    author='Anurag Gothi',
    author_email='ianuraggothi@gmail.com',
    keywords=['crypto-price', 'crypto-price-notifier',
              'crypto price', 'crypto', 'Crypto'],
    url='https://github.com/anurag-gothi-au6/cryptoprice-notifier',
    include_package_data=True
)

install_requires = [
    'requests'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
