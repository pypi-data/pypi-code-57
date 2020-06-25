from qiskit import *
from kaleidoscope.qiskit.backends import cnot_error_density
provider = IBMQ.load_account()

backends = provider.backends(simulator=False,
                             filters=lambda b: b.configuration().n_qubits == 5)

cnot_error_density(backends)