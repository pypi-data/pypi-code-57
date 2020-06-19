import numpy as np
import h5py
import hickle as hkl
import timeit

x = np.random.random((2000, 2000))
file=h5py.File('data.h5', 'w');file.create_dataset('x',data=x);file.close()
hkl.dump(x, 'data.hkl')
file=h5py.File('data_gzip.h5', 'w');file.create_dataset('x',data=x,compression='gzip');file.close()
hkl.dump(x, 'data_gzip.hkl', compression='gzip')
file=h5py.File('data_lzf.h5', 'w');file.create_dataset('x',data=x,compression='lzf');file.close()
hkl.dump(x, 'data_lzf.hkl',compression='lzf')

a = timeit.timeit("file=h5py.File('data.h5', 'r');x=file['x'][:];file.close()",
              setup="import numpy as np;import h5py", number=1000)/1000
print(a)
b = timeit.timeit("x=hkl.load('data.hkl')",
              setup="import numpy as np; import hickle as hkl", number=1000)/1000
print(b)

e = timeit.timeit("file=h5py.File('data_lzf.h5', 'r');x=file['x'][:];file.close()",
              setup="import numpy as np;import h5py", number=100)/100
print(a)
f = timeit.timeit("x=hkl.load('data_lzf.hkl')",
              setup="import numpy as np; import hickle as hkl", number=100)/100
print(b)