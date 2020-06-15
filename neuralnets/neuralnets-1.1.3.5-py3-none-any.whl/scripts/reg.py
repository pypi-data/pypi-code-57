import numpy as np
import tifffile as tiff
import os

from neuralnets.util.io import num2str, read_tif


def write_translated(data, zs, dir_path):

    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    mxb = int(np.abs(np.min(zs[:, 0])))
    mxe = int(np.abs(np.max(zs[:, 0])))
    myb = int(np.abs(np.min(zs[:, 1])))
    mye = int(np.abs(np.max(zs[:, 1])))
    orig_sz = data.shape[1:]
    new_sz = (int(orig_sz[0] + mxb + mxe), int(orig_sz[1] + myb + mye))

    for z in range(data.shape[0]):
        z_str = num2str(z, K=4)
        new_data = np.zeros(new_sz)
        xstart = int(mxb+zs[z, 0])
        xstop = int(mxb+data.shape[1]+zs[z, 0])
        ystart = int(myb+zs[z, 1])
        ystop = int(myb+data.shape[2]+zs[z, 1])
        new_data[xstart:xstop, ystart:ystop] = data[z, :, :]
        tiff.imsave(dir_path + '/' + z_str + '.tif', new_data.astype('uint8'))


# load volume
data_file = '/home/jorisro/Desktop/regdata/HPF_1705_FIBreg.tif'
data = read_tif(data_file)
z = data.shape[0]
print(data.shape)

# random shifts
dir_path = '/home/jorisro/Desktop/regdata/rnd_shifts'
sigma = 10
zs = np.round(sigma * (np.random.rand(z, 2) - 0.5))
# write_translated(data, zs, dir_path)

# constant x shift, increasing y shift
dir_path = '/home/jorisro/Desktop/regdata/inc_y_shift'
x_sigma = 5
y_sigma = 5
y_min = 0
y_max = 50
zsx = np.round(x_sigma * (np.random.rand(z, 1) - 0.5))
zsy = np.round(np.linspace(y_min, y_max, num=z)[..., np.newaxis] + y_sigma * (np.random.rand(z, 1) - 0.5))
zs = np.concatenate((zsx, zsy), axis=1)
write_translated(data, zs, dir_path)

# constant y shift, increasing x shift
dir_path = '/home/jorisro/Desktop/regdata/inc_x_shift'
x_sigma = 5
x_min = 0
x_max = 50
y_sigma = 5
zsx = np.round(np.linspace(x_min, x_max, num=z)[..., np.newaxis] + x_sigma * (np.random.rand(z, 1) - 0.5))
zsy = np.round(y_sigma * (np.random.rand(z, 1) - 0.5))
zs = np.concatenate((zsx, zsy), axis=1)
write_translated(data, zs, dir_path)
