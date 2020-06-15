# -*- coding: utf-8 -*-
"""
default parameters configuration
"""

MAX_IOU_DISTANCE = 0.95  # Kalman Filter IOU distance threshold
MAX_AGE = 20  # maxiumal count before discarding a track
N_INIT = 5  # minimal count before confirm a track
MAX_COSINE_DISTANCE = 0.0  # reid threshold, 0.0 is to disable reid part.
NN_BUDGET = 1  # reid gallery size for each ID
