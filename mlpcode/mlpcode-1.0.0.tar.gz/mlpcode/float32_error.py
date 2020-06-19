import numpy as np
# from numba import guvectorize
from typing import Union
import time

# @guvectorize(
#     ['void(boolean[:], int64, int64, boolean[:])'],
#     '(n),(),()->(n)', target='parallel'
# )

def _random_bit_flip(x: np.ndarray, n_bits, mode, newX):
    assert x.shape[1] == 32

    idx = np.arange(0, 32, dtype=np.int32)

    # If the MSB of the exponent field is high, ignore the rest of bits in the exponent field
    # The reason this bit comes at 25 instead of 1, is the little endian representation
    if x[25]:
        idx[26:32] = -1
        idx[16] = -1
    # Otherwise, ignore the MSB itself
    else:
        idx[25] = -1

    n = len(idx)
    if mode == 0:
        for i in range(n):
            if x[idx[i]]:
                idx[i] = -1
    elif mode == 1:
        for i in range(n):
            if not x[idx[i]]:
                idx[i] = -1

    idx = idx[idx != -1]
    if idx.size < n_bits:
        n_bits = idx.size
    idx = np.random.choice(idx, n_bits, replace=False)

    newX[idx] = ~x[idx]

# Unpacks the bits of each element in a numpy array
# Expected datatype is float32
def unpack(x: np.ndarray):
    res: np.ndarray = np.frombuffer(x, dtype=np.uint8)
    res = np.unpackbits(res)
    res = res.reshape(x.shape + (32, ))
    return res.astype(np.bool)


# Expected datatype is uint8
def repack(x: np.ndarray, shape: tuple):
    res: np.ndarray = np.packbits(x)
    res = np.frombuffer(res, dtype=np.float32).reshape(shape)
    return res

# Modes :
#   0 : Flip zeros to ones
#   1 : Flip ones to zeros
#   otherwise : Hybrid mode (flip ones to zeros and zeros to ones)
def random_bit_flip(x: Union[np.ndarray, np.float32], n_bits: int, mode: int):
    assert 0 < n_bits <= 32
    if isinstance(x, np.ndarray):
        newX = unpack(x.astype(np.float32))
        _random_bit_flip(newX, n_bits, mode, newX)
        newX = repack(newX, x.shape)
    else:
        newX = unpack(np.float32(x))
        _random_bit_flip(newX, n_bits, mode, newX)
        newX = repack(newX, (1, ))[0]

    return newX


x = 4 * np.random.random(10 ** 6) - 2
b = time.time()
y = random_bit_flip(x, 1, 2)
print(time.time() - b)
