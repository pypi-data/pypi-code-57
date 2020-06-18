import numpy as np
import math
from glob import glob
import random
import subprocess


def sampledist(n):
    d = np.random.lognormal(size=n)
    e = np.ones(np.size(d)) * math.e
    return np.power(e, d)


def rescaledist(d, r):
    s = np.sum(d)
    return np.round((r / s) * d)


def sampledirs(n, rdir):
    li = glob(rdir + "*/")
    if n > len(li):
        raise ValueError(f"Number of organisms specified is greater than available subfolders"
                         f" {n} organisms specified, {len(li)} folders available.")
    return random.sample(li, n)


def check_num_reads(folders, r_dist):
    flag = False
    problems = ""
    for f in folders:
        bashcommand = f"grep -c '>' {f}*_1* >> tmp.txt"
        subprocess.check_call(bashcommand, shell=True)
    with open("tmp.txt", "r") as f:
        for i in range(len(r_dist)):
            c = f.readline()
            if int(r_dist[i]) > int(c):
                flag = True
                problems += folders[i]
    # Clean up
    subprocess.check_call("rm tmp.txt", shell=True)
    return flag, problems
