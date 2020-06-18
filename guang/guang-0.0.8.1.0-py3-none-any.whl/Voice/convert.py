import os
from pydub import AudioSegment
from multiprocessing import Pool
from glob import glob


def cvt2wav(orig_path, new_path, sr=16000):
    basename = os.path.basename(orig_path)
    sufname = basename.split('.')[-1]

    x = AudioSegment.from_file(orig_path, format=sufname)
    x = x.set_channels(1)
    x = x.set_frame_rate(sr)
    x = x.set_sample_width(2)
    x.export(new_path, format='wav')


# def multi_cvt2wav(PATH_orig, PATH_new, sr=16000, n_cpu=None):
#     with Pool(processes=n_cpu) as pool:
#         for i,j in zip(PATH_orig, PATH_new):
#             pool.apply_async(cvt2wav, (i, j, sr))


def multi_cvt2wav(PATH1, PATH2, FORMAT='*', sr=16000, n_cpu=None):
    PATH_orig = glob(f"{PATH1}/*.{FORMAT}")
    if not os.path.exists(PATH2): os.makedirs(PATH2)
    PATH_new = [os.path.join(PATH2, os.path.basename(i)) for i in PATH_orig]

    pool = Pool(processes=n_cpu)
    for i, j in zip(PATH_orig, PATH_new):
        pool.apply_async(cvt2wav, (i, j, sr))
    pool.close()
    pool.join()


if __name__ == "__main__":
    multi_cvt2wav('data', "new_data")
