import numpy as np
from qiskit import *
from qiskit.quantum_info import Statevector

from kaleidoscope.interactive import bloch_disc
qc = QuantumCircuit(1)
qc.ry(np.pi*np.random.random(), 0)
qc.rz(np.pi*np.random.random(), 0)

state = Statevector.from_instruction(qc)
bloch_disc(state, as_widget=True)