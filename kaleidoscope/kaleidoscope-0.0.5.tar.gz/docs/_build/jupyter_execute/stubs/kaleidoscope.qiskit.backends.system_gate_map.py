from qiskit import *
from kaleidoscope.qiskit.backends import system_gate_map

pro = IBMQ.load_account()
backend = pro.backends.ibmq_vigo
system_gate_map(backend, as_widget=True)