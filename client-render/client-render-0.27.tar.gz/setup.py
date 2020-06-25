import os

from setuptools import setup, find_packages

requires = []
with open('REQUIREMENTS', 'r') as f:
    requires.extend(f.readlines())


def _read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        return f.read()


setup(
    version="0.27",
    name="client-render",
    license='MIT',
    description=_read('DESCRIPTION'),
    author="Nikolay Telepenin",
    author_email="telepenin.nikolay@gmail.com",
    url="https://github.com/telepenin/client-render/",
    classifiers=[
        'Topic :: Multimedia :: Graphics :: 3D Rendering',
        'Intended Audience :: Developers',
        'Environment :: Win32 (MS Windows)',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    long_description=_read('README.md'),
    install_requires=requires,
    set_build_info=os.path.dirname(__file__),
    python_requires=">=3.7",
    scripts=['bin/render-cmd.bat'],
)
