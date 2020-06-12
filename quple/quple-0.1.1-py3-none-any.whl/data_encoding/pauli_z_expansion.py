from typing import Callable, Optional
import numpy as np

from quple.data_encoding.pauli_expansion import PauliExpansion

class PauliZExpansion(PauliExpansion):
    def __init__(self, feature_dimension: int,
                 depth: int=2, z_order:int = 2,
                 encoding_map:Optional[Callable[[np.ndarray], float]] = None,
                 name:str=None):
        '''Create PauliZExpansion feature map
        Args:
            feature_dimension: dimension of data to be encoded (=number of qubits in the circuit)
            depth: the number of repetition of the encoding circuit
            z_order: order of pauli z operations to be performed on each entangling block
            encoding_map: data mapping function from R^(feature_dimension) to R
            name: name of circuit
        '''        
        paulis = []
        for i in range(1, z_order + 1):
            paulis.append('Z' * i)
        super().__init__(feature_dimension, depth, paulis=paulis,
                         encoding_map=encoding_map, name=name)