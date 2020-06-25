from distutils.core import setup
import setuptools

try:
    from pypandoc import convert_file

    read_md = lambda f: convert_file(f, 'rst')
except ImportError:
    print('warning: pypandoc module not found, could not convert Markdown to RST')
    read_md = lambda f: open(f, 'r').read()


def convert_md_to_rst(fn):
    open_quote = False
    for line in read_md(fn).split('\n'):
        if not line.strip():
            continue
        if line.lstrip().startswith(':'):
            yield f' {line.strip()}'
        elif open_quote:
            open_quote = line.count('`') != 1  # see if closed
            yield f' {line.lstrip()}'
        elif line.count('`') == 1:
            yield f'\n{line.rstrip()}'
            open_quote = True
        else:
            yield f'\n{line}'


with open('README.rst', 'w') as out:
    out.write(''.join(convert_md_to_rst('README.md')))

setup(name='regexify',
      version='0.1.6',
      description='Regular expression containers and helper functions',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      url='https://github.com/dcronkite/regexify',
      author='dcronkite',
      author_email='dcronkite+pypi@gmail.com',
      license='MIT',
      classifiers=[  # from https://pypi.python.org/pypi?%3Aaction=list_classifiers
          'Development Status :: 4 - Beta',
          'Programming Language :: Python :: 3 :: Only',
          'License :: OSI Approved :: MIT License',
      ],
      entry_points={
          'console_scripts':
              [
              ]
      },
      install_requires=[],
      package_dir={'': 'src'},
      packages=setuptools.find_packages('src'),
      zip_safe=False,
      python_requires='>=3.7',
      )
