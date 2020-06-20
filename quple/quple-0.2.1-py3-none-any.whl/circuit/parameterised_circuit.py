from abc import ABC, abstractmethod
from inspect import signature
from typing import (Any, Callable, cast, Dict, FrozenSet, Iterable, Iterator,
                    List, Optional, overload, Sequence, Set, Tuple, Type,
                    TYPE_CHECKING, TypeVar, Union)
import sympy as sp

import cirq
from cirq.ops.gate_features import SingleQubitGate, TwoQubitGate

from quple.circuit.quantum_circuit import QuantumCircuit
from quple.circuit.templates.template_circuit_block import TemplateCircuitBlock
from quple.components.parameter_table import ParameterTable
from quple.components.connectivity_graphs import connectivity_graph
from pdb import set_trace
#D. Zhu, Training of quantum circuits on a hybrid quantum computer


#Devices generally operate in the Z basis, so that rotations around the Z axis will become book-keeping measures rather than physical operations on the device.

class ParameterisedCircuit(QuantumCircuit, ABC):
    def __init__(self, n_qubit:int, copies:int=1,
                rotation_blocks:Optional[Union[str, cirq.Gate, Callable, 'TemplateCircuitBlock',
                                               List[str],List[cirq.Gate],List[Callable],
                                               List['TemplateCircuitBlock']]] =None,
                entanglement_blocks:Optional[Union[str, cirq.Gate, Callable, 'TemplateCircuitBlock',
                                               List[str],List[cirq.Gate],List[Callable],
                                               List['TemplateCircuitBlock']]] =None,
                entangle_strategy:Optional[Union[str,List[str], Callable[[int,int],List[Tuple[int]]],
                                                 List[Callable[[int,int],List[Tuple[int]]]]]]=None,
                parameter_symbol:str='θ',
                final_rotation_layer:bool=False,
                name:str=None):
        super().__init__(n_qubit, name=name)
        self._copies = copies
        self.rotation_blocks = rotation_blocks
        self.entanglement_blocks = entanglement_blocks
        self._entangle_strategy = 'full' or entangle_strategy
        self._parameter_symbol = parameter_symbol
        self._dynamic_param = None
        self._final_rotation_layer = final_rotation_layer
        
    @property
    def copies(self) -> int:
        return self._copies
    
    @property
    def parameter_symbol(self) -> str:
        return self._parameter_symbol
    
    @property
    def entangle_strategy(self):
        return self._entangle_strategy
    
    @property
    def final_rotation_layer(self):
        return self._final_rotation_layer
    
    @property
    def rotation_blocks(self):
        '''A collection of single qubit gate operations or 
        circuit blocks consisting of multiple single qubit operations
        '''
        return self._rotation_blocks
    
    @rotation_blocks.setter
    def rotation_blocks(self, val):
        val = ParameterisedCircuit._parse_blocks(val)
        ParameterisedCircuit._validate_blocks(val, SingleQubitGate, allow_template=False)
        self._rotation_blocks = val
    
    @property
    def entanglement_blocks(self):
        '''A collection of two qubit gate operations or 
        circuit blocks consisting of multiple single/two qubit operations
        '''
        return self._entanglement_blocks
    
    @entanglement_blocks.setter
    def entanglement_blocks(self, val):
        val = ParameterisedCircuit._parse_blocks(val)
        ParameterisedCircuit._validate_blocks(val, TwoQubitGate)
        self._entanglement_blocks = val
        
    @staticmethod
    def _parse_blocks(blocks) -> List:
        if not blocks:
            return []
        blocks = [blocks] if not isinstance(blocks, list) else blocks
        blocks = [QuantumCircuit._parse_gate_operation(block) if
                  isinstance(block, str) else block for block in blocks]
        return blocks
    
    @staticmethod
    def _validate_blocks(blocks, gate_feature=None, allow_template=True) -> None:
        for block in blocks:
            if isinstance(block, TemplateCircuitBlock):
                if not allow_template:
                    raise ValueError('template circuit block is not allowed'
                                     'in rotation layer')
                else:
                    continue
            elif isinstance(block, cirq.Gate):
                if gate_feature and \
                    not isinstance(block, gate_feature):
                    raise ValueError('Gate operation {} should be a subclass of '
                                     '{}'.format(type(block), gate_feature))
            elif callable(block):
                n_param = ParameterisedCircuit._get_parameter_count(block)
                if not n_param:
                    raise ValueError('not a valid gate operation or'
                                     'circuit block: {}'.format(block))
                dummy_params = tuple(sp.symarray('x',n_param))
                ParameterisedCircuit._validate_blocks([block(*dummy_params)], gate_feature)
        
    @staticmethod
    def _get_parameter_count(gate_expr) -> int:
        '''Returns the number of parameters required for a gate operation expression
        a gate operation expression can be a cirq.Gate instance, a string that can be mapped
        to a cirq.Gate instance, a function that maps to cirq.Gate or a TemplateCircuitBlock instance
        '''
        if isinstance(gate_expr, cirq.Gate):
            return 0
        elif isinstance(gate_expr, TemplateCircuitBlock):
            return gate_expr.num_params
        elif callable(gate_expr):
            return len(signature(gate_expr).parameters)
        else:
            raise ValueError('invalid gate expression {} of type {}'.format(gate_expr, type(gate_expr)))
    
    def get_total_parameter_count(self) -> int:
        rotation_param_count = 0
        entanglement_param_count = 0
        for block in self._rotation_blocks:
            rotation_param_count += ParameterisedCircuit._get_parameter_count(block)*self.n_qubit
        for i, block in enumerate(self._entanglement_blocks):
            if isinstance(block, TemplateCircuitBlock):
                connectivity_graphs = self.get_connectivity_graphs(i, block.num_block_qubits)
            else:
                connectivity_graphs = self.get_connectivity_graphs(i, 2)
            entanglement_param_count += ParameterisedCircuit._get_parameter_count(block)*len(connectivity_graphs)
        param_count = (rotation_param_count+entanglement_param_count)*self.copies + \
                        rotation_param_count*self.final_rotation_layer
        return param_count
     
    def reserve_parameters(self) -> None:
        param_count = self.get_total_parameter_count()
        if param_count:
            self._parameter_table.append_array(self.parameter_symbol, param_count)
            self._dynamic_param = iter(self._parameter_table[self.parameter_symbol])
    
    @property
    def dynamic_param(self) -> Optional[Iterator]:
        return self._dynamic_param
    
    def new_param(self) -> sp.Symbol:
        param = next(self.dynamic_param, None)
        if param:
            return param
        else:
            raise ValueError('incorrect number of parameters used in the parameterised circuit')
    
    def new_layer(self, name:str=None):
        layer = super().new_layer(name=name)
        layer._parameter_symbol = self.parameter_symbol
        layer._parameter_table = self._parameter_table
        layer._dynamic_param = self._dynamic_param
        return layer
        
    #https://cirq.readthedocs.io/en/latest/google/best_practices.html
    @staticmethod
    def build_params_for_sweep(self):
        pass
    
    #https://cirq.readthedocs.io/en/latest/google/best_practices.html
    def flatten_sweep(self):
        pass
    
    
    def assemble(self):
        self.clear()
        self.reserve_parameters()
        for _ in range(self.copies):
            # can't just multiply since parameters won't get incremented
            self += self.get_rotation_layer()
            self += self.get_entanglement_layer()
        if self.final_rotation_layer:
            self += self.get_rotation_layer()
                         
    def get_connectivity_graphs(self, block_index:int, num_block_qubits:int, *args, **kwargs):
        strategy = self.entangle_strategy
        if isinstance(strategy, str):
            return connectivity_graph[strategy](self.n_qubit, num_block_qubits)
        elif callable(strategy):
            return strategy(self.n_qubit, num_block_qubits)
        elif isinstance(strategy, list):
            if all(isinstance(strat, str) for strat in strategy):
                return connectivity_graph[strategy[block_index]](self.n_qubit, num_block_qubits)
            elif all(callable(strat) for strat in strategy):
                return strategy[block_index](self.n_qubit, num_block_qubits)
        else:
            raise ValueError('invalid entangle strategy: {}'.format(strategy))
        
    # Devices are generally calibrated to circuits that alternate single-qubit gates with two-qubit gates in each layer. Staying close to this paradigm will often improve performance of circuits.

    def parameterise_gate(self, gate:Union[cirq.Gate, Callable]):
        if isinstance(gate, cirq.Gate):
            return gate
        else:
            n_param = ParameterisedCircuit._get_parameter_count(gate)
            params = tuple(self.new_param() for _ in range(n_param))
            return gate(*params)
    
    def get_rotation_layer(self):
        rotation_layer = self.new_layer('rotation_layer')
        for rotation_block in self.rotation_blocks:
            for qubit in range(self.n_qubit):
                gate = self.parameterise_gate(rotation_block)
                rotation_layer.apply_gate_operation(gate, qubit)
        return rotation_layer

    def get_entanglement_layer(self):
        entanglement_layer = self.new_layer('entanglement_layer')
        for i, entanglement_block in enumerate(self.entanglement_blocks):
            if isinstance(entanglement_block, TemplateCircuitBlock):
                connectivity_graphs = self.get_connectivity_graphs(i, entanglement_block.num_block_qubits)
                for qubits in connectivity_graphs:
                    entanglement_block.build(entanglement_layer, qubits)
            else:
                connectivity_graphs = self.get_connectivity_graphs(i, 2)
                for qubits in connectivity_graphs:
                    gate = self.parameterise_gate(entanglement_block)
                    entanglement_layer.apply_gate_operation(gate, qubits)
    
        return entanglement_layer
        