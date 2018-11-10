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
from modules import bitFlipError, phaseFlipError, shorsCode
import math
import argparse

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
    desired_state = [1/2, math.sqrt(3)/2]
    q, c, qc = bitFlipError(stateVector=[], error_probability=0.8)
    qc.measure(q,c)
    backend_sim = Aer.get_backend('qasm_simulator')
    job_sim = execute(qc, backend_sim)
    result_sim = job_sim.result()

    print("Measurement of decoded state:", result_sim)
    print(result_sim.get_counts(qc))
    # diagram = matplotlib_circuit_drawer(qc, filename='bit_flip_circuit.png')
    # diagram.show()
    

def test_phaseflip():
    # desired_state = [1/2, math.sqrt(3)/2]
    desired_state = [1, 0]
    q, c, qc = phaseFlipError(stateVector=desired_state, error_probability=0.8)
    qc.measure(q, c)
    backend_sim = Aer.get_backend('qasm_simulator')
    job_sim = execute(qc, backend_sim)
    result_sim = job_sim.result()

    print("Measurement of decoded state:", result_sim)
    print(result_sim.get_counts(qc))

    # diagram = matplotlib_circuit_drawer(qc, filename='phase_flip_circuit.png')
    # diagram.show()

def test_shorsCode():
    # desired_state = [1/2, math.sqrt(3)/2]
    desired_state = [1, 0]
    q, c, qc = shorsCode(stateVector=desired_state, error_probability=0.8)
    qc.measure(q, c)
    backend_sim = Aer.get_backend('qasm_simulator')
    job_sim = execute(qc, backend_sim)
    result_sim = job_sim.result()

    print("Measurement of decoded state:", result_sim)
    print(result_sim.get_counts(qc))
    # diagram = matplotlib_circuit_drawer(qc, filename='shors_code_circuit.png')
    # diagram.show()

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--error', required = True, type = str, choices = ['bitflip', 'phaseflip', 'shors'], help = "The type of error correction that is to be simulated.")
    parser.add_argument('--error_probability', required = False, type = float, default = 0.8, help = "The probability of there being an error in the qubits while transmission.")
    parser.add_argument('--desiredState', nargs = 2, type = float, help = "Amplitudes of the states 0 and 1 in the form of a list.")
    args = parser.parse_args()
    print(args)

    if args.error == 'bitflip':
        test_bitflip()
    elif args.error == 'phaseflip':
        test_phaseflip()
    elif args.error == 'shors':
        test_shorsCode()