from setuptools import setup, find_packages

setup(
    name='vrep-python',
    version='0.4',
    keywords = ('vrep', 'python'),
    description='vrep python library'.encode(),
    license='Free',
    author='chenyiming',
    author_email='cymcpak00@gmail.com',
    url='http://github.com/cpak00/vrep-python',
    platforms = 'any',
    packages = ['vrep', 'vrep.core'],
    package_data = {
        '': ['*.dll', '*so', '*.dylib']
    },
    install_requires = ['numpy', 'opencv-python>=3.4', 'opencv-contrib-python>=3.4']

    # packages = find_packages('./vrep'),
    # package_dir = {'':'./vrep'}
)
