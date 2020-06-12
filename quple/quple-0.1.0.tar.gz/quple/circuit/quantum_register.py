from cirq import GridQubit

from typing import (Any, Callable, cast, Dict, FrozenSet, Iterable, Iterator,
                    List, Optional, overload, Sequence, Set, Tuple, Type,
                    TYPE_CHECKING, TypeVar, Union)    


    
class QuantumRegister():
    def __init__(self, n_qubit=0):
        self._n_qubit = n_qubit
        self._qubits = [GridQubit(i, 0) for i in range(n_qubit)]

        
    def __getitem__(self, key: int) -> GridQubit:
        return self._qubits[key]
    
    @staticmethod
    def _is_unique_qubit_set(qubit_set: Union[List[Tuple[GridQubit]],Tuple[GridQubit]]):
        if isinstance(qubit_set, tuple):
            return len(set(qubit_set)) == len(qubit_set)
        elif isinstance(qubit_set, list):
            return all(len(set(qubit_subset)) == len(qubit_subset) for qubit_subset in qubit_set)
        return False
        

    @staticmethod
    def _parse_qubit_expression(qubit_expr, target_qubits:Sequence[GridQubit],
                               unique_set=True) -> Union[List[GridQubit], List[Tuple[GridQubit]]]:
        '''
        return list of qubits or list of tuples of qubits
        '''
        def check_uniqueness(qubit_sequence):
            for qubits in qubit_sequence:
                if isinstance(qubits, tuple) and \
                (not QuantumRegister._is_unique_qubit_set(qubits)):
                    raise ValueError('Qubits in the set {} are not unique'.format(qubits))
                
        resolved_qubits = None
        try:
            if isinstance(qubit_expr, GridQubit):
                resolved_qubits = [qubit_expr]
            elif isinstance(qubit_expr, int):
                resolved_qubits = [target_qubits[qubit_expr]]
            elif isinstance(qubit_expr, (range,list)) and \
            all(isinstance(expr, int) for expr in qubit_expr):
                resolved_qubits = [target_qubits[i] for i in qubit_expr]
            elif isinstance(qubit_expr, list) and \
            all(isinstance(expr, tuple) for expr in qubit_expr):
                resolved_qubits = [tuple(target_qubits[i] for i in qtuples) for qtuples in qubit_expr] 
            elif isinstance(qubit_expr, list) and \
            all(isinstance(expr, GridQubit) for expr in qubit_expr):
                resolved_qubits = qubit_expr
            elif isinstance(qubit_expr, tuple):
                resolved_qubits = [tuple(target_qubits[i] for i in qubit_expr)]
                QuantumRegister._is_unique_qubit_set(resolved_qubits)
            elif isinstance(qubit_expr, slice):
                resolved_qubits = target_qubits[qubit_expr]
            else:
                raise ValueError('Unsupported qubit expression {} ({})'.format(qubit_expr, type(qubit_expr)))
        except IndexError:
                raise IndexError('Qubit index out of range.') from None
        except TypeError:
                raise IndexError('Qubit index must be an integer') from None
        if unique_set:      
            check_uniqueness(resolved_qubits)
        return resolved_qubits
    
    @staticmethod
    def _neighbor_pair_sequence(target_qubits: Sequence[GridQubit]) -> List[Tuple[GridQubit]]:
        n_qubit = len(target_qubits)
        qubit_expr = [(i, i+1) for i in range(n_qubit-1)]
        return QuantumRegister._parse_qubit_expression(qubit_expr, target_qubits)
    
    def neighbor_pair_sequence(self) -> List[Tuple[GridQubit]]:
        return QuantumRegister._neighbor_pair_sequence(self._qubits)
    
    def get(self, qubit_expr) -> Union[List[GridQubit], List[Tuple[GridQubit]]]:
        return QuantumRegister._parse_qubit_expression(qubit_expr, self._qubits)
    
    @property
    def n_qubit(self) -> int:
        return self._n_qubit

    @property
    def qubits(self) -> List[GridQubit]:
        return self._qubits    