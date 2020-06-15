# This script illustrates how to analyze a labeled dataset
import os

import numpy as np

from neuralnets.util.io import read_volume, write_volume

# path to the data and the corresponding type
data_path = '/home/jorisro/research/data/EM/VIB/Project_093_WimAnnaert/2017_04_07_Po93_6Q_46'
type = 'pngseq'

# analyze the data
for ds in ['registered']:
    # read the data
    data = read_volume(os.path.join(data_path, ds), type=type)
    # measure size
    sz = data.shape
    # report
    print("Dataset %s: " % (ds))
    print("    Size: %d x %d x %d" % (sz[0], sz[1], sz[2]))
