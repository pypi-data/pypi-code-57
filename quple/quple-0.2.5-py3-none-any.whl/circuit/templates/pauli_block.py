from typing import Sequence

from quple.circuit.templates.template_circuit_block import TemplateCircuitBlock


class PauliBlock(TemplateCircuitBlock):
    def __init__(self, pauli_string:str):
        self.paulis = pauli_string[::-1]
        self.indices = [i for i, pauli in enumerate(self.paulis) if pauli != 'I']
        self._num_block_qubits = len(self.paulis)
    
    @staticmethod
    def change_basis(circuit:'EncodingCircuit', qubits:Sequence[int],
                     pauli_string:Sequence[str], inverse=False) -> None:
        for i, pauli in enumerate(pauli_string):
            if pauli == 'X':
                circuit.H(qubits[i])
            elif pauli == 'Y':
                circuit.RX(-np.pi / 2 if inverse else np.pi / 2, qubits[i])            

    def build(self, circuit:'EncodingCircuit', qubits:Sequence[int]):
        if not self.indices:
            return None
        
        PauliBlock.change_basis(circuit, qubits, self.paulis)
        
        qubits_to_entangle = tuple(qubits[i] for i in self.indices)
        encoded_value = circuit.encode_parameters(list(qubits))
        circuit.entangle(qubits_to_entangle)    
        circuit.RZ(2.0*encoded_value, qubits[-1])
        circuit.entangle(qubits_to_entangle, inverse=True)

        PauliBlock.change_basis(circuit, qubits, self.paulis, inverse=True)       
    
    @property
    def num_params(self) -> int:
        return 0
    
    @property
    def num_block_qubits(self) -> int:
        return self._num_block_qubits