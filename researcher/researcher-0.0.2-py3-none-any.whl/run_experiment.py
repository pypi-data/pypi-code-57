import os
import random
import datetime
import argparse

import tensorflow as tf
import numpy as np

from researcher.logging import *
from researcher.experiment import *

seed_value= 78876 
os.environ['PYTHONHASHSEED']=str(seed_value)
random.seed(seed_value)
np.random.seed(seed_value)
tf.random.set_seed(seed_value) 

tf.get_logger().setLevel('ERROR')
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus: 
    tf.config.experimental.set_memory_growth(gpu, True)


parser = argparse.ArgumentParser()
parser.add_argument(
    "mode", 
    help="run experiment and record results to tensorboard or run in trial mode", 
    choices=["train", "trial"],
    type=str
)
parser.add_argument(
    "savepath", 
    help="the directory where experiments should be saved", 
    type=str
)
parser.add_argument(
    "logpath", 
    help="the directory where logs should be stored", 
    type=str
)
parser.add_argument(
    "--skip", 
    help="experiments from the queue to skip", 
    nargs="+",
    default=[]
)
parser.add_argument(
    "--sources", 
    help="a list of filenames to read parameters from", 
    nargs="+",
    default="tf_queue.json"
)


args = parser.parse_args()

param_queue = []

for source in args.sources:
    with open(source) as f:
        param_queue += json.load(f)["queue"]

param_queue = [params for params in param_queue if params["description"] not in args.skip]

print("prepairing to run the following experiments:")
for params in param_queue:
    process_params(params) # to confirm (somewhat) that params are not invalid

    print(params["description"])

print("\n\n")

if args.mode == "train":
    for params in param_queue:
        run_param_kfold_experiment(params)

if args.mode == "trial":
    for params in param_queue:
        run_param_kfold_experiment(params, test=True, max_samples=200)