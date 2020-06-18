from qiskit import *
from kaleidoscope.qiskit.backends import system_error_map

pro = IBMQ.load_account()
backend = pro.backends.ibmq_vigo
system_error_map(backend, as_widget=True)