from typing import List, Sequence, Union, Optional, Tuple
import itertools 
from pdb import set_trace
import cirq

from quple.circuit.quantum_circuit import QuantumCircuit


class EntanglementCircuit(QuantumCircuit):
    def __init__(self, n_qubit:int, name:str=None) -> None:
        super().__init__(n_qubit, name=name)
    
    @staticmethod
    def _validate_entangler_map(n_qubit:int, n_block_qubit:int) -> None:
        if n_block_qubit > n_qubit:
            raise ValueError('The number of qubits in a block'
            'cannot exceed the total number of qubits in the circuit.')

    @staticmethod
    def _get_entangler_map(n_qubit:int, n_block_qubit:Optional[int]=2,
                          method:str='full') -> List[Sequence[int]]:
        '''
        Args:
            n_qubit: number of qubits in the circuit
            n_block_qubit: number of qubits in a block
            method: method of entanglement
                -'full': all combination of qubit pairs are entangled
                -'linear': neighboring qubit pairs are entangled
        '''
        EntanglementCircuit._validate_entangler_map(n_qubit, n_block_qubit)
        n, m = n_qubit, n_block_qubit
        entangler_map = None
        if method == 'full':
            entangler_map =  list(itertools.combinations(list(range(n)), m))
        elif method == 'linear':
            entangler_map =  [tuple(range(i, i + m)) for i in range(n - m + 1)]
        elif method == 'circular':
            entangler_map = [tuple(range(n - m + 1, n)) + (0,)]
            entangler_map += [tuple(range(i, i + m)) for i in range(n - m + 1)] #linear part
            
        return entangler_map
    
    def get_entangler_map(self, n_block_qubit:Optional[int]=2, method:str='full') -> List[Tuple]:
        '''Get the entangler map
        An entangler map defines the entanglement blocks in a circuit, 
        inside an entanglement block, multiple qubits are entangled and
        a parametrised gate operation may act on one of these entangled qubits.
        For example, for a 4 qubit system with 5 parametrised variables
        an entangler map may be:
        [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
        i.e. there are a total of 4 entanglement blocks
        in the block (0, 1, 2), qubits 0, 1, 2 are entangled
        and an Rz rotation maybe performed on one of the qubits with the
        angle parametrised by the variables x[0], x[1] and x[2]
        the above entangler map will have all combinations of entanglement with 3 qubits,
        thus it's a 'full' entanglement
        how the 3 qubits are entangled is defined by the function _entangled_qubit_pairing
        Args:
            n_block_qubit: number of qubits in a block (value of 1 means no entanglement)
            method: method of entanglement
        Returns:
        '''
        entangler_map = EntanglementCircuit._get_entangler_map(self.n_qubit, n_block_qubit, method)
        return entangler_map
    
    def _entangled_qubit_pairing(self, qubits: Sequence[int]):
        '''determines how qubits are paired in the entanglement operation
        can be overridden
        Args:
            qubits: qubits to be entangled
        Return:
            list of pair of qubit indices for entanglement
        Example:
        >>> cq = EntanglementCircuit(n_qubit=5)
        >>> cq._entangled_qubit_pairing((1,3,4)) #entangle qubits 1, 3 and 4
        [(1,3), (3,4)]
        '''
        pairing_indices = [(qubits[i], qubits[i+1]) for i in range(len(qubits)-1)]
        
        return pairing_indices
    
    def entangle(self, qubits:Sequence[int],
                 inverse:bool=False,
                 operation:cirq.Gate=cirq.ops.CNOT):
        '''entangle qubits in a quantum cirquit
        Args:
            qubits: qubits to be entangled
            inverse: reverse the order of operation
            operation: gate operation that entangles the qubits
        Example:
        >>> cq = EntanglementCircuit(n_qubit=5)
        >>> cq.entangle((1,2))
        >>> cq.entangle((0,3,4))
                       ┌──┐
            (0, 0): ─────@────────
                         │
            (1, 0): ────@┼────────
                        ││
            (2, 0): ────X┼────────
                         │
            (3, 0): ─────X────@───
                              │
            (4, 0): ──────────X───
                       └──┘
        '''
        
        pairing_indices = self._entangled_qubit_pairing(qubits)
        qubit_pairs = self._qubits.get(pairing_indices)
        if inverse:
            qubit_pairs = qubit_pairs[::-1]
        self.append([operation(*qpair) for qpair in qubit_pairs])  
        
    '''
    def get_entangled_qubits(self) -> Set[Int]:
        entangled_qubits = set()        
    '''