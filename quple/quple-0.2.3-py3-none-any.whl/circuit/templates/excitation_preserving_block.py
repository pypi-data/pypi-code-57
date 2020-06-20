from typing import Sequence
import numpy as np

from quple import TemplateCircuitBlock

class ExcitationPreservingBlock(TemplateCircuitBlock):
    def __init__(self, mode:str='iswap'):
        supported_modes = ['iswap', 'fsim']
        if mode not in supported_modes:
            raise ValueError('Unsupported mode {}, choose one of {}'.format(mode, supported_modes))
        self.mode = mode
    
    @staticmethod
    def RYY(circuit:'ParameterisedCircuit', theta, qubits:Sequence[int]):
        circuit.RX(np.pi/2, list(qubits))
        circuit.CX(tuple(qubits))
        circuit.RZ(theta, qubits[1])
        circuit.CX(tuple(qubits))
        circuit.RX(-np.pi/2, list(qubits))
        
    @staticmethod
    def RXX(circuit:'ParameterisedCircuit', theta, qubits:Sequence[int]):
        circuit.H(list(qubits))
        circuit.CX(tuple(qubits))
        circuit.RZ(theta, qubits[1])
        circuit.CX(tuple(qubits))
        circuit.H(list(qubits))
        

    def build(self, circuit:'ParameterisedCircuit', qubits:Sequence[int]):
        theta = circuit.new_param()
        ExcitationPreservingBlock.RXX(circuit, theta, qubits)
        ExcitationPreservingBlock.RYY(circuit, theta, qubits)
        if self.mode == 'fsim':
            phi = circuit.new_param()
            circuit.CZ(phi, qubits)    
    
    @property
    def num_params(self) -> int:
        return 2
    
    @property
    def num_block_qubits(self) -> int:
        return 2