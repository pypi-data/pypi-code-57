from distutils.core import setup

setup(
    name = 'lalgebra',
    packages = ['lalgebra'],
    version = '0.1.2',
    license='MIT',
    description = 'Includes basic support for points, lines and vectors',
    long_description="See github page.",
    long_description_content_type="text/markdown",
    author = 'Jonathan Tan Jiayi',
    author_email = 'jonathantanatlol@gmail.com',
    url = 'https://github.com/peaceknight05/linear',
    download_url = 'https://github.com/peaceknight05/linear/archive/v0.1.2.tar.gz',
    keywords = ['mathematics', 'linear algebra', 'algebra', 'topography', 'geometry', 'vectors', 'lines', 'points'],
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)