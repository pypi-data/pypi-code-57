import numpy as np
from qiskit import *
from qiskit.quantum_info import Statevector
from kaleidoscope.interactive import bloch_multi_disc

N = 4
qc = QuantumCircuit(N)
qc.h(range(N))
for kk in range(N):
    qc.ry(2*np.pi*np.random.random(), kk)
for kk in range(N-1):
    qc.cx(kk,kk+1)
for kk in range(N):
    qc.rz(2*np.pi*np.random.random(), kk)

state = Statevector.from_instruction(qc)
bloch_multi_disc(state, as_widget=True)