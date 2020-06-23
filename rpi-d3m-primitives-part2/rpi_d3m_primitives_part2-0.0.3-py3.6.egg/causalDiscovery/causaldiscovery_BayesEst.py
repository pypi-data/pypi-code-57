import numpy as np
import pandas as pd
import pydot
from pycausal.pycausal import pycausal as pc 
from pycausal import search as s
from rpi_d3m_primitives_part2.pyBN.learning.structure.naive.TAN import TAN
from rpi_d3m_primitives_part2.pyBN.classes.bayesnet import BayesNet


def Edges_to_DAG_BN(V, E, D):
    # N = len(V)
    dag = np.zeros((D, D))
    for e in E:
        parent, child = e.split(' --> ')
        # dag[int(parent)-1, int(child)-1] = 1
        dag[int(parent), int(child)] = 1
    return dag

def causaldiscovery_BayesEst(train_data, train_labels, java_max_heap_size = '500M', depth = -1, alpha = 0.05, verbose = False):
    trainMatrix = np.concatenate( [train_data, train_labels.reshape(-1,1)], 1) # trainMatrix size M*d, M samples, D variables
    D = trainMatrix.shape[1]
    data = pd.DataFrame(trainMatrix) # the columns of data is 0, 1, 2, ..., D-1

    # py-causal BayesEst method
    from pycausal.pycausal import pycausal as pc 
    pc = pc()
    pc.start_vm(java_max_heap_size = java_max_heap_size)
    from pycausal import search as s
    try:
        print('First attempt to perform global causal discovery.\n')
        bayesEst = s.bayesEst(data, depth = depth, alpha = alpha, verbose = verbose) # check if the input data need to be a Dataframe?
        V = bayesEst.getNodes() # '0', '1', '2', ..., 'D-1' 
        E = bayesEst.getEdges() # '0 --> 1'
        pc.stop_vm()
        dag_learned = Edges_to_DAG_BN(V, E, D) # index should be the varialbe number
    except:
        try: 
            print('Second attempt to perform global causal discovery.\n')
            bayesEst = s.bayesEst(data, depth = depth, alpha = alpha, verbose = verbose) # check if the input data need to be a Dataframe?
            V = bayesEst.getNodes() # '0', '1', '2', ..., 'D-1' 
            E = bayesEst.getEdges() # '0 --> 1'
            pc.stop_vm()
            dag_learned = Edges_to_DAG_BN(V, E, D) # index should be the varialbe number
        except:
            try: 
                print('Third attempt to perform global causal discovery.\n')
                bayesEst = s.bayesEst(data, depth = depth, alpha = alpha, verbose = verbose) # check if the input data need to be a Dataframe?
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

    return dag_learned

