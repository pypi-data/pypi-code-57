from uedge.hdf5 import *

fname='junk.foo'
status = False

try:
   status=hdf5_restore(fname)
except:
   pass
print("file open status=", status,fname)

fname='./test/level_2/data/junk.h5'
try:
    status = hdf5_restore(fname)
except:
    pass
print("file open status=", status,fname)
