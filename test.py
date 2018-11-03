'''
    Import: qiskit
        - QuantumCircuit: Class to create a quantum circuit.
        - QuantumRegister: Class to define a quantum register of n qubits.
        - ClassicalRegister: Class to define a classical register of n bits.
        - execute: Provides functionality to execute the quantum circuit on the various backends provided.
        - Aer: Provides simulator backends.
'''
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer
from qiskit.tools.visualization import circuit_drawer
# Creates a Quantum Register with 2 qubits.
q = QuantumRegister(2)

# Creates a Classical Register with 2 bits.
c = ClassicalRegister(2)

# Creates a Quantum Circuit using the quantum and classical registers.
qc = QuantumCircuit(q, c)

## Performing some operations on the circuit.
# Apply an H gate on the first qubit and putting this qubit in a superposition state.
qc.h(q[0])

# Measuring the state of the system
qc.measure(q, c)

# backend_sim = Aer.get_backend('qasm_simulator')
# job_sim = execute(qc, backend_sim)
# result_sim = job_sim.result()

# print("Simulation: ", result_sim)
# print(result_sim.get_counts(qc))

# Provide a name to write the diagram to the filesystem
circuit_drawer(qc, filename='./bell_circuit.png')

# Use the return value with show() to display the diagram
diagram = circuit_drawer(qc)
diagram.show()