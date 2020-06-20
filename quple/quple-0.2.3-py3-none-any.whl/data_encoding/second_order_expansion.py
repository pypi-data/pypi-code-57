from typing import Callable, Optional
import numpy as np

from quple.data_encoding.pauli_z_expansion import PauliZExpansion

class SecondOrderExpansion(PauliZExpansion):
    def __init__(self, feature_dimension: int,
                 depth: int=2, 
                 encoding_map:Optional[Callable[[np.ndarray], float]] = None,
                 name:str=None):
        '''Create Second Order Expansion feature map
        Args:
            feature_dimension: dimension of data to be encoded (=number of qubits in the circuit)
            depth: the number of repetition of the encoding circuit
            encoding_map: data mapping function from R^(feature_dimension) to R
            name: name of circuit
        '''        
        super().__init__(feature_dimension, depth, z_order=2,
                         encoding_map=encoding_map, name=name)