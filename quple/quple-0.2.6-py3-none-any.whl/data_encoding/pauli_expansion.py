from typing import List, Union, Optional, Callable, Sequence
import numpy as np
from pdb import set_trace

import cirq

from quple.circuit.quantum_circuit import QuantumCircuit
from quple.data_encoding.encoding_circuit import EncodingCircuit
from quple.circuit.templates.pauli_block import PauliBlock

class PauliExpansion(EncodingCircuit):
    '''PauliExpansion feature map

    '''    
    def __init__(self, feature_dimension: int,
                 copies: int=2, paulis:List[str] = ['Z', 'ZZ'],
                 encoding_map:Optional[Callable[[np.ndarray], float]] = None,
                 name:str=None):
        '''Create PauliExpansion encoder circuit
        Args:
            feature_dimension: dimension of data to be encoded (=number of qubits in the circuit)
            depth: the number of repetition of the encoding circuit
            paulis: pauli operations to be performed on each entangling block
            encoding_map: data mapping function from R^(feature_dimension) to R
            name: name of circuit
        '''
        PauliExpansion._validate_paulis(paulis)
        pauli_blocks = [PauliBlock(pauli) for pauli in paulis]
        super().__init__(feature_dimension, copies, 
                         entanglement_blocks=pauli_blocks,
                         encoding_map=encoding_map, name=name)
        self.paulis = paulis
        
    @staticmethod
    def _validate_paulis(paulis:List[str]):
        for pauli_str in paulis:
            for pauli in pauli_str:
                if pauli not in ['Z','X','Y','I']:
                    raise ValueError('Invalid Pauli operation: {}'.format(pauli))