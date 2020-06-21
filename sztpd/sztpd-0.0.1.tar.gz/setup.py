import io
import os
import sys
import setuptools
#from glob import glob
from setuptools.command.sdist import sdist

# a combination of:
#  -  https://realpython.com/pypi-publish-python-package
#  -  https://github.com/kennethreitz/setup.py/blob/master/setup.py

NAME = "sztpd"
HERE = os.path.abspath(os.path.dirname(__file__))
#HERE = pathlib.Path(__file__).parent

# Import the README.md and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
with io.open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


# Load the package's __version__.py module as a dictionary.
about = {}
with open(os.path.join(HERE, 'src', NAME, '__version__.py')) as f:
    exec(f.read(), about)
with open(os.path.join(HERE, 'README.md')) as f:
    about['__long__'] = f.read()
#README = (HERE / "README.md").read_text()

#def read_text(file_name: str):
#    return open(os.path.join(base_path, file_name)).read()


class CustomSdistCommand(sdist):
    def run(self):
        import git
        import subprocess
        import python_minifier
        from os import listdir
        #from pyang.translators import yang as yang_translator

        # ensure all files checked in
        repo = git.Repo("./")
        if len(repo.index.diff(None)) > 0:
            print("\nPlease commit files and try again.")
            return

        # minimize the .py files
        #FIXME: any way to remove all the comments in the YANG files?
        for fn in listdir("src/sztpd"):
            if fn.endswith('.py'):
                print("Processing " + fn + "...")
        
                with open("src/sztpd/"+fn, mode='r') as f:
                    minified = python_minifier.minify(f.read(), filename=fn, remove_literal_statements=True)

                with open("src/sztpd/"+fn, mode='w') as f:
                    f.write("# Copyright (c) 2020 Watsen Networks.  All Rights Reserved.\n\n")
                    f.write(minified)


        # strip comments out of YANG files
        for fn in listdir("src/sztpd/yang"):
            if fn.startswith('wn-'):
                print("Processing " + fn + "...")
                subprocess.run(["pyang", "-f", "yang", "--yang-remove-comments", "src/sztpd/yang/"+fn, "-o", "src/sztpd/yang/"+fn])

#pyang -f yang --yang-remove-comments $i -o $i

# OLD PYANG module-based approach (SHOULD FIX!)
#        # strip comments out of YANG files
#        yang_translator = YANGPlugin()
#        yang_translator.add_opts(["--yang-remove-comments"])
#        ctx = 
#
#        for filename in filenames:
#            try:
#                fd = io.open(filename, "r", encoding="utf-8")
#                text = fd.read()
#                module = ctx.add_module(filename, text)
#
#            text = sys.stdin.read()
#            module = ctx.add_module('<stdin>', text)
#
#          fd = open...
#          yang_translator.emit(ctx?, modules?, fd?)


        # let normal sdist process run
        sdist.run(self)

        # restore Git files to original state
        head = repo.heads[0]
        head.checkout(force=True)


# Where the magic happens:
setuptools.setup(
    name=NAME,
    description="Secure Zero Touch Provisioning Daemon (SZTPD)",
    #long_description=long_description,
    long_description=about['__long__'],
    long_description_content_type='text/markdown',
    license='Non Production License',
    #license_file="LICENSE",
    url="https://watsen.net/products/sztpd",
    author="Watsen Networks",
    author_email="info@watsen.net",
    project_urls={
      "Documentation": "https://watsen.net/docs/sztpd",
      "License": "https://watsen.net/sales/non-production-use.html"
      #"Bug Tracker": "https://bugs.example.com/HelloWorld/",
      #"Source Code": "https://code.example.com/HelloWorld/",
    },
    version=about['__version__'],
    python_requires=">=3.7.*, <4",
    package_dir = {"": "src"},
    packages=setuptools.find_packages("src"),
    #py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    #packages=['src/sztpd'],
    #package_dir={'sztpd': 'src/sztpd'},
    package_data={'sztpd': ['LICENSE.txt', 'yang/*.yang']},
    #include_package_data = True,
    keywords = ["IETF", "SZTP", "RFC 8572", "secure", "zerotouch", "zero touch", "provisioning", "ztp"],
    install_requires=['six', 'sqlalchemy', 'sqlalchemy_utils', 'pysqlite3', 'cryptography', 'yangson', 'aiohttp==3.6.2', 'basicauth', 'pyasn1', 'pyasn1-modules', 'pem', 'passlib', 'requests', 'certvalidator'],
    #extras_require=EXTRAS,
    #setup_requires = ["pytest-runner"],
    #tests_require = ["pytest"],
    entry_points = { "console_scripts": ["sztpd=sztpd.__main__:main"] },
    classifiers = [
      # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
      "Development Status :: 3 - Alpha",
      "Environment :: Console",
      "Intended Audience :: Information Technology",
      "Intended Audience :: System Administrators",
      "Intended Audience :: Telecommunications Industry",
      "License :: Other/Proprietary License",
      "Natural Language :: English",
      "Operating System :: OS Independent",
      "Programming Language :: Python",
      "Programming Language :: Python :: 3",
      "Programming Language :: Python :: 3.7",
      "Programming Language :: Python :: 3.8",
      "Topic :: Communications",
      "Topic :: Internet",
      "Topic :: Security"
    ],
    cmdclass={
        'sdist': CustomSdistCommand
    }
)

