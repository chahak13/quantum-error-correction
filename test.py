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
from qiskit.tools.visualization import circuit_drawer, matplotlib_circuit_drawer
from modules import *

def test():
    # Creates a Quantum Register with 2 qubits.
    def circuit():
        q = QuantumRegister(1)

        # Creates a Classical Register with 2 bits.
        c = ClassicalRegister(1)

        # Creates a Quantum Circuit using the quantum and classical registers.
        qc = QuantumCircuit(q, c)
        ## Performing some operations on the circuit.
        # Apply an H gate on the first qubit and putting this qubit in a superposition state.
        qc.h(q[0])
        return q,c,qc
    
    q,c,qc = circuit()
    print(qc)
    # qc.cx(q[1])
    # Measuring the state of the system
    qc.measure(q, c)

    backend_sim = Aer.get_backend('qasm_simulator')
    job_sim = execute(qc, backend_sim)
    result_sim = job_sim.result()

    print("Simulation: ", result_sim)
    print(result_sim.get_counts(qc))

    # Provide a name to write the diagram to the filesystem
    # circuit_drawer(qc, filename='./bell_circuit.png')

    # Use the return value with show() to display the diagram
    diagram = matplotlib_circuit_drawer(qc)
    diagram.show()

def test_bitflip():
    q, c, qc = bitFlipError()
    # import pdb; pdb.set_trace()
    # Measuring the state of the system
    # qc.measure(q, c)

    # backend_sim = Aer.get_backend('qasm_simulator')
    # job_sim = execute(qc, backend_sim)
    # result_sim = job_sim.result()

    # print("Simulation: ", result_sim)
    # print(result_sim.get_counts(qc))

    # diagram = matplotlib_circuit_drawer(qc, filename='bit_flip_circuit.png')
    # diagram.show()
    
if __name__ == '__main__':
    
    # test()
    test_bitflip()
