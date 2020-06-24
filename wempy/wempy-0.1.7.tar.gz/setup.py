from distutils.core import setup
import codecs

def readme(filename):
    in_file = codecs.open(filename, 'r')
    return in_file.read()

files = ["wemplate/*"]

setup(name = "wempy",
    version = "0.1.7",
    description = "Embedded python interpreter (very similar to Ruby's erb).",
    author = "G. Clifford Williams",
    author_email = "gcw@notadiscussion.com",
    license = "LGPLv3",
    url = "http://www.wempy.org/",
    packages = ['wemplate'],
    package_data = {'wemplate' : [
                                    'LICENSE',
                                    'README.rst',
                                    'README.wiki',
                                    'wemplate/*.py',
                                    'wempy',
                                    ]
                    },
    scripts = ["wempy"],
    long_description = readme('README.rst'),
    python_requires='>=2.7',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: Jython',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Text Processing :: Filters',
    ]     
) 
