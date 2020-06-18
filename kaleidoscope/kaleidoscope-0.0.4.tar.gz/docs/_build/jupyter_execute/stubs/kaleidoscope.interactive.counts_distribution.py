from kaleidoscope.qiskit.overload import QuantumCircuit
from kaleidoscope.qiskit.providers import simulators
from kaleidoscope.interactive import counts_distribution

sim = simulators.aer_vigo_simulator

qc = QuantumCircuit(3, 3) >> sim
qc.h(1)
qc.cx(1,0)
qc.cx(1,2)
qc.measure(range(3), range(3))

counts = qc.transpile().sample().result_when_done()
counts_distribution(counts, as_widget=True)