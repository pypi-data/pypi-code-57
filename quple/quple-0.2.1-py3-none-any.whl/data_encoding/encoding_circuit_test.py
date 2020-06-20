from abc import ABC, abstractmethod
from typing import Optional, List, Union, Callable
import numpy as np

import cirq

from quple import ParameterisedCircuit
from quple.data_encoding.encoding_maps import self_product

class EncodingCircuit(ParameterisedCircuit, ABC):
    '''The data encoding circuit
    A parametrised quantum circuit for encoding classical data into quantum states
    Examples:
    >>> cq = EncodingCircuit(5, depth=1, param_symbol='x')
    '''
    def __init__(self, feature_dimension:int, copies:int=1,
                 encoding_map:Optional[Callable[[np.ndarray], float]] = None,
                 parameter_symbol:Optional[str]=None, name:str=None):
        '''Create a new Pauli expansion circuit.
        Args:
            feature_dimension: dimension of data to be encoded (=number of qubits in the circuit)
            depth: the number of repetition of the encoding circuit
            encoding_map: data mapping function from R^(feature_dimension) to R
            parameter_symbol: the symbol for the unresolved parameter array
            name: name of circuit
        '''
        super().__init__(n_qubit=feature_dimension, copies=copies, 
                         parameter_symbol=parameter_symbol, name=name)
        self._feature_dimension = feature_dimension
        self._encoding_map = encoding_map or self_product
        self._parameter_table.append_array(self._parameter_symbol, feature_dimension)
        
    def get_parameters(self, indices:List[int]):
        '''Obtain parameter symbols corresponding to the array indices
        Args:
            indices: array indices of the parameter
        Return:
            parameter symbols
        Example:
        >>>  cq.get_parameters((1,2))
        (x[1], x[2])
        '''
        return self._parameter_table[self._parameter_symbol][indices]

    def encode_parameters(self, indices:List[int]):
        '''Obtain the encoded value for the given parameters using the encoding map
        Args:
            indices: indices of parameter array which corresponds to the indices of qubits in the circuit
        Returns:
            symbolic representation of the encoded data using the encoding map
        Example:
        >>> from quple.data_encoding.PauliExpansion import PauliExpansion
        >>> cq = PauliExpansion(feature_dimension=5, depth=1)
        >>> cq.encode_parameters(indices=(0,2,4))
        >>> (np.pi-x[0])*(np.pi-x[2])*(np.pi-x[4])
        '''
        parameters = self.get_parameters(indices)
        encoded_value = self.encoding_map(parameters)
        return encoded_value

    @property
    def parameter_symbol(self):
        return self._parameter_symbol
    
    @property
    def feature_dimension(self):
        return self._feature_dimension
    
    
    @property
    def encoding_map(self):
        return self._encoding_map