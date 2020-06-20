from distutils.core import setup, Extension
import os
import sys

version = os.environ.get('PYDINEMIC_VERSION')
boost_lib = None
for arch in ('arm-linux-gnueabihf', 'x86_64-linux-gnu'):
  if os.path.exists('/usr/lib/' + arch + '/libboost_python3.so'):
      boost_lib = 'boost_python3'
      break
  elif os.path.exists('/usr/lib/' + arch + '/libboost_python37.so'):
      boost_lib = 'boost_python37'
      break
  elif os.path.exists('/usr/lib/' + arch + '/libboost_python-py37.so'):
      boost_lib = 'boost_python-py37'
      break
  elif os.path.exists('/usr/lib/' + arch + '/libboost_python3-py37.so'):
      boost_lib = 'boost_python3-py37'
      break
  elif os.path.exists('/usr/lib/' + arch + '/libboost_python-py35.so'):
      boost_lib = 'boost_python-py35'
      break
  elif os.path.exists('/usr/lib/' + arch + '/libboost_python-py35.so'):
      boost_lib = 'boost_python-py35'
      break
      
if boost_lib is None:
    print('Failed to find boost::python libraries. Check in your system')
    sys.exit(1)

pydinemic = Extension('dinemic',
                      sources=['src/dinemic/module.cpp',
                               'src/dinemic/pyaction.cpp',
                               'src/dinemic/pydfield.cpp',
                               'src/dinemic/pydlist.cpp',
                               'src/dinemic/pyddict.cpp',
                               'src/dinemic/pydmodel.cpp'],
                      include_dirs=['/usr/include', 'src/pydinemic'],
                      library_dirs=['/usr/lib/x86_64-linux-gnu/'],
                      runtime_library_dirs=['/usr/lib/x86_64-linux-gnu/'],
                      libraries=[boost_lib, 'dinemic'])


setup(name='dinemic',
      author='cloudover.io ltd.',
      version='20.05.15',
      description='Dinemic framework for python',
      package_dir={'': 'src'},
      packages=['pkg'],
      headers=['src/dinemic/module.h',
               'src/dinemic/pyaction.h',
               'src/dinemic/pydfield.h',
               'src/dinemic/pydlist.h',
               'src/dinemic/pydmodel.h',
               'src/dinemic/pyaction.h'],
      ext_modules=[pydinemic])
