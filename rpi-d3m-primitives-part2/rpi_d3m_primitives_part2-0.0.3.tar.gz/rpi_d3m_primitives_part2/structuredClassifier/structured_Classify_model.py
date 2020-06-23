import sys
import os
import numpy as np
import pandas as pd
import pydot
# from rpi_d3m_primitives.structuredClassifier.learnCPD import learnCPDAllD
# from rpi_d3m_primitives.structuredClassifier.inference import posteriorInf
# from rpi_d3m_primitives.pyBN.learning.structure.naive.naive_bayes import naive_bayes
from rpi_d3m_primitives_part2.pyBN.learning.structure.naive.TAN import TAN
from rpi_d3m_primitives_part2.pyBN.classes.bayesnet import BayesNet
# from rpi_d3m_primitives.pyBN.learning.structure.score.hill_climbing import hc as hill_climbing
# from rpi_d3m_primitives.pyBN.learning.structure.score.tabu import tabu as tabu
#from rpi_d3m_primitives.pyBN.learning.structure.constraint.grow_shrink import gs as grow_shrink
#from rpi_d3m_primitives.pyBN.learning.structure.hybrid.mmhc import mmhc
# from CMU py-causal model, should have been pre-installed
from pycausal.pycausal import pycausal as pc 
from pycausal import search as s
from rpi_d3m_primitives_part2.structuredClassifier.helper import Edges_to_DAG_BN, BayesNetToDag
from pgmpy.base import DAG
from pgmpy.models import BayesianModel 
from pgmpy.estimators import MaximumLikelihoodEstimator 
from pgmpy.inference import VariableElimination
# from pyBN.learning.structure.naive.TAN import TAN
# from pyBN.classes.bayesnet import BayesNet

import pickle


class Model():
    
    def __init__( self, java_max_heap_size = '500M', depth = -1, alpha = 0.05, verbose = False):
        # store parameters
        self.java_max_heap_size = java_max_heap_size
        self.depth = depth
        self.alpha = alpha
        self.verbose = verbose
        # store learned parameters
        self.D = None
        self.structure_fit = None
        self.structure = None # put learned dag here
        self.BN = None # put learned Bayesian Network here, with structure and parameters

    
    def learnStructure( self, train_data, train_labels, **kwargs):
        
        trainMatrix = np.concatenate( [train_data, train_labels.reshape(-1,1)], 1) # trainMatrix size M*d, M samples, D variables
        D = trainMatrix.shape[1]
        self.D = D
        data = pd.DataFrame(trainMatrix) # the columns of data is 0, 1, 2, ..., D-1

        # py-causal BayesEst method
        from pycausal.pycausal import pycausal as pc 
        pc = pc()
        pc.start_vm(java_max_heap_size = self.java_max_heap_size)
        from pycausal import search as s
        try:
            print('First attempt to perform global causal discovery.\n')
            bayesEst = s.bayesEst(data, depth = self.depth, alpha = self.alpha, verbose = self.verbose) # check if the input data need to be a Dataframe?
            V = bayesEst.getNodes() # '0', '1', '2', ..., 'D-1' 
            E = bayesEst.getEdges() # '0 --> 1'
            pc.stop_vm()
            dag_learned = Edges_to_DAG_BN(V, E, D) # index should be the varialbe number
        except:
            try: 
                print('Second attempt to perform global causal discovery.\n')
                bayesEst = s.bayesEst(data, depth = self.depth, alpha = self.alpha, verbose = self.verbose) # check if the input data need to be a Dataframe?
                V = bayesEst.getNodes() # '0', '1', '2', ..., 'D-1' 
                E = bayesEst.getEdges() # '0 --> 1'
                pc.stop_vm()
                dag_learned = Edges_to_DAG_BN(V, E, D) # index should be the varialbe number
            except:
                try: 
                    print('Third attempt to perform global causal discovery.\n')
                    bayesEst = s.bayesEst(data, depth = self.depth, alpha = self.alpha, verbose = self.verbose) # check if the input data need to be a Dataframe?
                    V = bayesEst.getNodes() # '0', '1', '2', ..., 'D-1' 
                    E = bayesEst.getEdges() # '0 --> 1'
                    pc.stop_vm()
                    dag_learned = Edges_to_DAG_BN(V, E, D) # index should be the varialbe number
                except:
                    print('Causal Discovery Failed, switch to Tree-augmented method.\n')
                    tan_BN = TAN(trainMatrix, D-1)
                    dag_learned = BayesNetToDag(tan_BN)

        if np.sum(dag_learned, axis = 0)[-1] == 0:
            del dag_learned
            print('The causal discovery results do not include target variables, switch to Tree-augmented method.\n')
            tan_BN = TAN(trainMatrix, D-1)
            dag_learned = BayesNetToDag(tan_BN)
        self.structure = dag_learned
        self.structure_fit = True

    def learnParameters( self, train_data, train_labels, debug= False):
        if self.structure_fit == True:
            trainMatrix = np.concatenate( [train_data, train_labels.reshape(-1,1)], 1)
            D = trainMatrix.shape[1]
            data = pd.DataFrame(trainMatrix) # the columns of data is 0, 1, 2, ..., D-1
            G = DAG(self.structure)
            self.BN = BayesianModel()
            self.BN.add_nodes_from(nodes = G.nodes())
            self.BN.add_edges_from(ebunch = G.edges())
            self.BN.fit(data, estimator = MaximumLikelihoodEstimator)
        else:
            raise ValueError("The model need to perform structure learning first.\n")
            

        
    def fit( self, train_data, train_labels, debug= False, **kwargs):
        self.learnStructure( train_data, train_labels, **kwargs)   
        # self.learnParameters( train_data, train_labels, self.bayesInf, self.PointInf)  
        self.learnParameters( train_data, train_labels, **kwargs) 
        
    def predict( self, test_data):
        pred_data = pd.DataFrame(test_data)
        Y_est = self.BN.predict(pred_data).values
        return Y_est

def main():

    # load train data and train label
    # data_dir = "~/data/D3M/LL0_1100_popularkids/1100_train.pkl"
    # data_dir = "~/data/D3M/27_wordLevels/27_nbins5_quantile.pkl"
    # data_dir = "~/data/D3M/LL0_186_braziltourism/186_nbins_9.pkl"
    data_dir = "~/data/D3M/57_hypothyroid/57_nbins_2.pkl"
    with open(data_dir, 'rb') as f:
        train_data, train_labels = pickle.load(f)

    # create model, train the model and predict the target label
    clf = Model()
    clf.fit(train_data, train_labels)
    Y_est = clf.predict(train_data)

if __name__ == '__main__':
    main()