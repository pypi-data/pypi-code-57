import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='skxcs',
    version='0.1',
    license='MIT',
    author='Jaroslav Michalovcik',
    author_email='j.michalovcik@gmail.com',
    description='SciKit learn wrapper for XCS algorithm implementation.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    # url="",
    packages=setuptools.find_packages(),
    keywords=['XCS', 'xcs', 'SciKit', 'learn'],
    install_requires=[
        'numpy',
        'pandas',
        'mdlp',
        'sklearn',
        'xcs',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
    ],
    python_requires='>=3.7',
)
