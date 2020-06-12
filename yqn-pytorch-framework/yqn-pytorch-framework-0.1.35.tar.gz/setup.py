from distutils.core import setup

from setuptools import find_packages

# read the contents of the README
with open('README.md') as README_md:
    README = README_md.read()

if __name__ == '__main__':
    setup(
        name='yqn-pytorch-framework',
        version='0.1.35',
        author='James Guo',
        author_email="james.guo89@gmail.com",
        description='YQN Pytorch Framework',
        url='https://www.google.com',
        long_description=README,
        long_description_content_type="text/markdown",
        license='Proprietary',
        package_data={'yqn_cli': ['template/*/*', ]},
        packages=find_packages(exclude=['tests', '*.tests', '*.tests.*']),
        install_requires=['opencv_python>=4.2.0.32',
                          'numpy>=1.18.2',
                          'torch>=1.4.0',
                          'torchvision>=0.5.0',
                          'nvidia_ml_py3>=7.352.0',
                          'setuptools>=41.2.0',
                          'oss2>=2.9.1',
                          'Pillow>=6.2.0',
                          'jieba>=0.39',
                          'pynvml>=8.0.4',
                          'PyYAML>=5.3', ],
        entry_points={
            'console_scripts': [
                'yqn-module = yqn_cli.init_model:main',
                'yqn-model = yqn_ops.download_resource:main'
            ],
        },
        keywords=' '.join([
            'pytorch', 'framework'
        ]),
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Environment :: Web Environment',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            "License :: OSI Approved :: MIT License",
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Programming Language :: Python',
            'Topic :: Communications :: Email',
            'Topic :: Office/Business',
            'Topic :: Software Development :: Bug Tracking',
        ],
    )
