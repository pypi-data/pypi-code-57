from typing import List, Union, Optional, Callable, Sequence
import numpy as np
from pdb import set_trace

import cirq

from quple import QuantumCircuit, TemplateCircuitBlock
from quple.data_encoding.encoding_circuit import EncodingCircuit

     
                

class PauliExpansion(EncodingCircuit):
    '''PauliExpansion feature map

    '''    
    def __init__(self, feature_dimension: int,
                 depth: int=2, paulis:List[str] = ['Z', 'ZZ'],
                 encoding_map:Optional[Callable[[np.ndarray], float]] = None,
                 name:str=None):
        '''Create PauliExpansion feature map
        Args:
            feature_dimension: dimension of data to be encoded (=number of qubits in the circuit)
            depth: the number of repetition of the encoding circuit
            paulis: pauli operations to be performed on each entangling block
            encoding_map: data mapping function from R^(feature_dimension) to R
            name: name of circuit
        '''
        super().__init__(feature_dimension, depth, encoding_map, name=name)
        self.paulis = paulis
        
    @staticmethod
    def _validate_paulis(paulis:List[str]):
        for pauli_str in paulis:
            for pauli in pauli_str:
                if pauli not in ['Z','X','Y','I']:
                    raise ValueError('Invalid Pauli operation: {}'.format(pauli))
        
    @property
    def paulis(self):
        return self._paulis
    
    @paulis.setter
    def paulis(self, value):
        PauliExpansion._validate_paulis(value)
        self._paulis = value
    
    @staticmethod
    def change_basis(circuit:QuantumCircuit, qubits:Sequence[int],
                     pauli_string:Sequence[str], inverse=False) -> None:
        for i, pauli in enumerate(pauli_string):
            if pauli == 'X':
                circuit.H(qubits[i])
            elif pauli == 'Y':
                circuit.RX(-np.pi / 2 if inverse else np.pi / 2, qubits[i])
    
    
                
        
        
    def _build_primary_layer(self):
        # build the Hadamard layer
        # this maps the |0>^n state into a superposition of 2^n states of equal weight
        # i.e. to the computational basis
        self.H(range(self._n_qubit))
                     
        # build the entanglement layer
        for pauli_string in self.paulis:
            pauli_string = pauli_string[::-1]
            n_pauli = len(pauli_string)
            indices = [i for i, pauli in enumerate(pauli_string) if pauli != 'I']
            if not indices:
                continue
                
            entangler_map = self.get_entangler_map(n_pauli, method='full')
            for qubits in entangler_map:
                
                PauliExpansion.change_basis(self, qubits, pauli_string)
                qubits_to_entangle = tuple(qubits[i] for i in indices)
                encoded_value = self.encode_parameters(qubits) 
                
                self.entangle(qubits_to_entangle)    
                self.RZ(2.0*encoded_value, qubits[-1])
                self.entangle(qubits_to_entangle, inverse=True)
                
                PauliExpansion.change_basis(self, qubits, pauli_string, inverse=True)
        
def self_product(x: np.ndarray) -> float:
    """
    Define a function map from R^n to R.

    Args:
        x: data

    Returns:
        float: the mapped value
    """
    coeff = x[0] if len(x) == 1 else reduce(lambda m, n: m * n, np.pi - x)  
    return coeff
