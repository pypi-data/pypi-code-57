from typing import Sequence
import numpy as np

from quple.circuit.quantum_circuit import QuantumCircuit


def change_rz_basis(circuit:QuantumCircuit, qubits:Sequence[int], pauli_string:str, inverse=False) -> None:
    '''re-express a parametrised rotation along X and Y axis in terms of 
    parametrised rotation along Z axise
    Example:
        Rx(pi-x[0]) == H\otimes Rz(pi-x[0]) \otimes H
    '''
    for i, pauli in enumerate(pauli_string):
        if pauli == 'X':
            circuit.H(qubits[i])
        elif pauli == 'Y':
            circuit.Rx(-np.pi / 2 if inverse else np.pi / 2, i)

            
            
            
def google_device_layouts(name):
    if name == 'Syncamore':
        return cirq.google.Syncamore
    elif name == 'Sycamore23':
        return cirq.google.Sycamore23
    elif name == 'Bristlecone':
        return cirq.google.Bristlecone
    elif name == 'Foxtail':
        return cirq.google.Foxtail