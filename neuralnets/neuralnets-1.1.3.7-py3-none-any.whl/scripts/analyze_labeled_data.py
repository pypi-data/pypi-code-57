# This script illustrates how to analyze a labeled dataset
import os

import numpy as np

from neuralnets.util.io import read_volume, write_volume

# path to the data and the corresponding type
data_path = '/home/jorisro/research/data/EM/VIB/Project_103_Patrizia/2018_03_16_P103_shPerk_bQ'
type = 'pngseq'

# analyze the data
for ds in ['train_labels', 'test_labels', 'val_labels']:
    # read the data
    data = read_volume(os.path.join(data_path, ds), type=type)
    # count labels
    cnt_bg = np.sum(data == 0)
    cnt_mito = np.sum(data == 1)
    cnt_er = np.sum(data == 2)
    cnt_nm = np.sum(data == 3)
    cnt_na = np.sum(data > 3)
    sz = data.shape
    # report
    print("Dataset %s: " % (ds))
    print("    Size: %d x %d x %d" % (sz[0], sz[1], sz[2]))
    print("    Label count (abs): BG (%d) - MITO (%d) - ER (%d) - NUCMEM (%d) - NA (%d)" % (
    cnt_bg, cnt_mito, cnt_er, cnt_nm, cnt_na))
    print("    Label count (rel): BG (%f) - MITO (%f) - ER (%f) - NUCMEM (%f) - NA (%f)" % (
        cnt_bg / data.size, cnt_mito / data.size, cnt_er / data.size, cnt_nm / data.size, cnt_na / data.size))
