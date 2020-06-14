import setuptools

from pter import version


with open('README.md', encoding='utf-8') as fd:
    long_description = fd.read()


with open('LICENSE', encoding='utf-8') as fd:
    licensetext = fd.read()


setuptools.setup(
    name='pter',
    version=version.__version__,
    description="Console UI to manage your todo.txt file(s).",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://git.spacepanda.se/bold-kitty/pter",
    author="R",
    author_email="devel+pter@kakaomilchkuh.de",
    entry_points={'console_scripts': ['pter=pter.main:run']},
    packages=['pter'],
    install_requires=['pytodotxt>=1.0'],
    extras_require={'xdg': ['pyxdg']},
    python_requires='>=3.0',
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Console :: Curses',
                 'Intended Audience :: End Users/Desktop',
                 'License :: OSI Approved :: MIT License',
                 'Natural Language :: English',
                 'Programming Language :: Python :: 3',])

