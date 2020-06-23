import numpy as np
import pandas as pd
import os
import pydot
# from IPython.display import SVG
# import timeit
from pycausal.pycausal import pycausal as pc
from pycausal import search as s
import sys
import scipy.io as sio 
from rpi_d3m_primitives_part2.pyBN.classes.bayesnet import BayesNet

def Edges_to_DAG_BN(V, E, D):
	# N = len(V)
	dag = np.zeros((D, D))
	for e in E:
		parent, child = e.split(' --> ')
		# dag[int(parent)-1, int(child)-1] = 1
		dag[int(parent), int(child)] = 1
	return dag

def BayesNetToDag(BayesNet):
	# input: BayesNet is a BayesNet object of pyBN package
	# Output: a matrix shows the relationship of Nodes
	DAG = np.zeros((len(BayesNet.E), len(BayesNet.E)))
	for N in BayesNet.V:
		for v in BayesNet.E[N]:
			DAG[N,v] = 1
	return DAG